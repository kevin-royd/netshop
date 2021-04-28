# 全局上下文

# 孤立文件，需要放置主配置文件中
def getUserInfo(request):
    return {'suser': request.session.get('user', None)}
