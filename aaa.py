import math

def paginated_hero(objs, all_args, options={}):
    print(all_args)
    args = dict(all_args)
    if "page" in args:
        try:
            page = int(args["page"])
            args.pop("page")
        except:
            page = 1
    else:
        page = 1
        
    
    pp=12
    if "per_page" in options:
        pp = int(options["per_page"])
    elif "per_page" in args:
        pp =  int(args["per_page"])
    else:
        args["per_page"] = pp

   
    offset = (page-1) * pp
    results = objs[offset:offset+pp]
    # Step 2
    pages = list(range(1, math.ceil(len(objs)/pp)+1))

    the_pagination = {
        "pages": pages,
        "results": results,
        "args": args

    }
    return the_pagination