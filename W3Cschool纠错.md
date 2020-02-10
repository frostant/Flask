# W3Cschool纠错

## 为什么？

因为在学习Flask的过程中参考W3Cschool教程，遇到了一个又一个奇奇怪怪的错误，头皮发麻。为了给后人铺平道路，写下该《W3Cschool纠错》一文

## Flask路由

该app.add_url_rule('/','hello',hello_world)中首先是中文符号，其次，第一个参数是url（网址）而第二个参数我还不知道有什么作用。但其表述让我一直误以为是第二个参数是网址即和第一段语句功能相同

## FlaskURL构建

首先，这段代码的import有所变换。他的\_\_name\__和\_\_main__因为markdown变成加粗。他的/user/后没有参数接口应改为/user/<name>，同理/guest/改为/guest/<guest>



