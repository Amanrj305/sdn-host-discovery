from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, arp, ipv4
import time


class HostDiscovery(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(HostDiscovery, self).__init__(*args, **kwargs)
        self.host_db = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Table-miss rule → send packets to controller
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        mod = parser.OFPFlowMod(datapath=datapath,
                               priority=priority,
                               match=match,
                               instructions=inst)

        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        # Ignore LLDP
        if eth.ethertype == 0x88cc:
            return

        src = eth.src
        dpid = datapath.id

        ip_addr = None
        arp_pkt = pkt.get_protocol(arp.arp)
        ip_pkt = pkt.get_protocol(ipv4.ipv4)

        # Extract IP
        if arp_pkt:
            ip_addr = arp_pkt.src_ip
        elif ip_pkt:
            ip_addr = ip_pkt.src

        # Host discovery (balanced logic)
        if src not in self.host_db:
            self.logger.info(f"New Host Detected: {src}")
            self.host_db[src] = {
                "ip": ip_addr,
                "switch": dpid,
                "port": in_port,
                "last_seen": time.time()
            }
        else:
            if ip_addr is not None:
                self.host_db[src]["ip"] = ip_addr

            self.host_db[src]["switch"] = dpid
            self.host_db[src]["port"] = in_port
            self.host_db[src]["last_seen"] = time.time()

        # FLOW RULE (FIXED)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        actions = [
            parser.OFPActionOutput(ofproto.OFPP_FLOOD),
            parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)
        ]

        match = parser.OFPMatch(in_port=in_port, eth_src=src)

        self.add_flow(datapath, 1, match, actions)

        self.display_hosts()

    def display_hosts(self):
        print("\n===== HOST DATABASE =====")
        for mac, data in self.host_db.items():
            print(f"{mac} -> {data}")
        print("=========================\n")
