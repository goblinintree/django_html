import copy

from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet 
from django.utils.safestring import mark_safe

class Pagination:
    """
    pagination = Pagination(request, query_set)
    context = {
        "pretty_list":pagination.page_query_set,
        "page_outhtml":pagination.html(),
        "q":req_q,
    }

    <div class="clearfix">
        <ul class="pagination">
            {{page_outhtml}}
        </ul>
    </div>
    """
    def __init__(self, request: WSGIRequest,query_set:QuerySet, page_param="page", size_param="pagesize"):
        self.page_param = page_param
        self.size_param = size_param
        self.request_get_copy  = copy.deepcopy(request.GET) 
        self.request_get_copy._mutable=True

        req_page = self.request_get_copy.get(self.page_param) # 获得当前页
        req_pagesize = self.request_get_copy.get(self.size_param) # 获得当前页
        print("=="*20)
        print(type(req_pagesize))
        print(req_pagesize)

        self.req_page = int(req_page) if req_page and req_page.isdecimal() else 1
        self.req_pagesize = int(req_pagesize) if req_pagesize and req_pagesize.isdecimal() else 10
        self.query_set =query_set
        # 分页
        self.query_set_total_count = query_set.count()
        quo, rem =  divmod(self.query_set_total_count,self.req_pagesize)
        self.total_page = quo+1 if rem else quo             # 总页数
        # 限定分页范围
        self.req_page = self.req_page   if self.req_page > 1 else 1
        self.req_page = self.total_page if self.req_page > self.total_page else self.req_page
        # 取数
        self.start = (self.req_page -1) * self.req_pagesize # 当前页开始行
        self.end = self.req_page * self.req_pagesize        # 当前页结束行
        self.page_query_set = query_set[self.start:self.end] # 分页数据集

        print("=="*10, req_page, req_pagesize)
        pass

    def html(self):
        self.start_page = self.req_page - 4 # 初始预期
        self.end_page   = self.req_page + 5 # 初始预期
        if self.start_page < 1:
            self.start_page = 1
            self.end_page = min(self.start_page+9, self.total_page)  
        
        if self.end_page > self.total_page:
            self.start_page = max(self.total_page-9, 1)
            self.end_page = self.total_page
        outhtml_list = []
        #  
        first_page_string = '<li {}> <a href="?{}" aria-label="Previous"><span aria-hidden="true">首页</span></a></li>'
        last_page_string  = '<li {}> <a href="?{}" aria-label="Next"><span aria-hidden="true">末页</span></a></li>'
        jump_string = """
                    <li style="border: 0;">
                        <form action="" style="float: left;" method="get" novalidate>
                            
                            <input type="text" name="page"  style="position: relative;width: 60px;display: inline-block;" id="jump" class="form-control" value="{}" required="required">
                            <button type="submit" class="btn btn-default" >跳转</button>
                        </form>

                    </li>
                    """
        # 首页
        self.request_get_copy.setlist(self.page_param,["1"])
        request_urlencode = self.request_get_copy.urlencode()
        if self.req_page == 1 :
            outhtml_list.append(first_page_string.format(' class="disabled" ',request_urlencode))
        else:
            outhtml_list.append(first_page_string.format("",request_urlencode))
        # 页码
        for num in range(self.start_page,self.end_page+1):
            self.request_get_copy.setlist(self.page_param,[str(num)])
            request_urlencode = self.request_get_copy.urlencode()
            if self.req_page == num :
                outhtml_list.append('<li class="active" style="width:60px;"><a href="?{}">{}<span class="sr-only">(current)</span></a></li>'.format(request_urlencode, num))
                pass
            else:
                outhtml_list.append('<li style="width:60px;"><a href="?{}">{}</a></li>'.format(request_urlencode, num))
                pass
            pass
        
        # 末页
        self.request_get_copy.setlist(self.page_param,[str(self.total_page)])
        request_urlencode = self.request_get_copy.urlencode()
        if self.req_page == self.total_page :
            outhtml_list.append(last_page_string.format(' class="disabled" ',request_urlencode))
        else:
            outhtml_list.append(last_page_string.format("",request_urlencode))
        outhtml_list.append(jump_string.format(str(self.req_page)))
        return mark_safe(''.join(outhtml_list))
            
        

        


        

    pass
