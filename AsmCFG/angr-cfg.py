import angr

def get_proj_all_path(file_path, functions_list):
    proj = angr.Project(file_path, load_options={'auto_load_libs':False})
    cfg_dict = {}
    for function in functions_list:
        function_obj = proj.loader.main_object.get_symbol(function)
        start_state = proj.factory.blank_state(addr=function_obj.rebased_addr)
        cfg = proj.analyses.CFGEmulated(keep_state=True,
                                        starts=(function_obj.rebased_addr,),
                                        initial_state=start_state,
                                        call_depth=0)
        cfg=cfg.get_function_subgraph(start=function_obj.rebased_addr, max_call_depth=0)
        cfg_dict[function]=cfg
    return cfg_dict

def print_graph(binfile, functions):
    CFGs = get_proj_all_path(binfile,functions)
    for function in CFGs:
        nodes = CFGs[function].graph.nodes()
        edges = CFGs[function].graph.out_edges()      
        for node in nodes:
            name = node.name  #节点的名字
            ins_addr_list = node.instruction_addrs
            addr = node.addr  #节点的地址
            size = node.size
            instruction = node.block.pp()  #该节点的指令

            # print(CFGs[function].get_topological_order(node))
            # print(node.instruction_addrs)
            # codenode = node.to_codenode()


if __name__ == '__main__':
    main()