# 注意

请调用本API的所有app将自己的`User-Agent`设置为`应用名:版本号:联系方式`的形式，例如`MyApp:0.1:admin@doufm.info`，方便进行管理。


# API 文档
## Web 端:  登录API

### URL:`/api/oauth/request/`

* Method `GET`:获取request_token

    * Arguments:None

    * Response:
        * `status`:操作是否成功
        * `authorize_url`:睿思授权页面

---

## App 端:  登录API

### URL:`/api/app_auth/`

* Method `POST`:用户登录

    * Arguments:
        * `user_name`: 用户名
        * `password`: 用户密码(密码要采用MD5编码，并采用小写格式)
    * Response:
        * `status`:登录状态，如果登录成功返回`success`, 否则返回出错原因,出错原因包括：
          `already login`:用户已经登录;
          `can not get rs response`: 无法与睿思连接;
        * `user_id`:用户id
        * `user_name`:用户名

---

## music API

### URL: `/api/music/`

* Method `GET`: 搜索歌曲

    * Arguments: 
        * `key`: 歌曲key
        * `title`: 歌曲名
        * `artist`: 艺术家
        * `album`: 专辑
        * `company`: 唱片公司
        * `public_time`: 出版年份
        * `kbps`: 码率
        * `start`, `end`: 起始, 终止

    * Response:
        
        歌曲列表，其中每一条目为一首歌曲，歌曲信息:
        * `key`: 歌曲key
        * `title`: 歌曲名
        * `artist`: 艺术家
        * `album`: 专辑
        * `company`: 唱片公司
        * `public_time`: 出版年份
        * `kbps`: 码率
        * `cover`: 专辑封面URL
        * `audio`: 音频URL
        * `upload_date`: 上传时间

    * Notes:
        * 当参数为空时，返回歌曲列表概述：
            * `/api/music/`:
                ```
                {
                    "count": 10
                }
                ```
        * 允许多条件查询
            * `/api/music/?title=title1`: 搜索歌曲名为title1的
            * `/api/music/?title=title1&kbps=64`: 搜索歌曲名为title1且码率为64kbps的歌曲
        * 使用参数`start`, `end`按范围查询歌曲
            * `/api/music/?start=0&end=2`: 获取前两首歌曲
            * `/api/music/?start=0`: 获取全部歌曲（慎用）

---

## channel API

### URL: `/api/channel/`

* Method `GET`: 获取分类列表
    * level: None

    * Arguments: 
        * `key`: 分类key
        * `name`: 分类名
        * `playable`: 是否显示在播放列表中
        * `start`, `end`: 起始, 终止

    * Response:
        
        歌曲分类列表，其中每一条目为一个分类，分类信息:
        * `key`: 分类key
        * `name`: 分类名
        * `music_list`: 分类中歌曲数
        * `update_num`: 本分类每日更新数量
        * `playable`: 是否显示在播放列表中
        * `upload_date`: 分类创建时间时间

    * Notes:
        * 当参数为空时，返回概述：
            * `/api/channel/`:
                ```
                {
                    "count": 10
                }
                ```
        * 条件查询
            * `/api/channel/?name=name1`: 搜索分类名为title1的分类
        * 使用参数`start`, `end`按范围查询分类
            * `/api/channel/?start=0&end=2`: 获取前两首分类
            * `/api/channel/?start=0`: 获取全部分类

---

## user API

### URL: `/api/user/logout/`

* Method `GET`:退出登录
    * Response:
        * `status`:如果退出成功则返回`success`, 如果用户还没有登录则返回:`have not login`

---

### URL: `/api/user/profile/`

* Method `GET`: 获取用户基本信息, 要求:用户用户必须登录，否则返回None
    * Response:
        * `favor`:用户喜欢的歌曲数量
        * `share`:用户分享的歌曲数量
        * `dislike`:用户不喜欢的歌曲数量
        * `listened`:用户听过的歌曲数量

---
### URL: `/api/user/history/`

* Method `GET`: 获取用户操作历史记录, 要求:用户用户必须登录，否则返回None
    * Arguments: 
        * `start`: 起始点
        * `end`: 终止点
    * Response:
        若未登录返回None，否则返回历史信息列表:
        * `data`: 日期
        * `op`: 操作
        * `key`: 歌曲ID
        * `title`: 歌曲名
        * `cover`: 封面key
        * `audio`: 歌曲key

* Method `POST`: 添加用户操作历史记录, 注意，如果对歌曲进行重复操作即表示取消原先的操作。要求:用户用户必须登录，否则返回None
    * Arguments: 
        * `op`: 操作类型(操作类型分别为：favor，dislike，shared，listened)
        * `key`: 歌曲ID
    * Response:
        * `status`:操作成功则返回`success`

---
### URL: `/api/user/music/`

* Method `GET`: 获取用户相关的歌曲列表。要求:用户用户必须登录，否则返回None
    * Arguments: 
        * `type`: 操作类型
        * `start`: 起点
        * `end`: 终点

    * Response:
        返回相关的音乐列表:
        * `key`: 歌曲key
        * `title`: 歌曲名
        * `artist`: 艺术家
        * `album`: 专辑
        * `company`: 唱片公司
        * `public_time`: 出版年份
        * `kbps`: 码率
        * `cover`: 专辑封面URL
        * `audio`: 音频URL

---
## playlist API

### URL: `/api/playlist/`

* Method `GET`: 获取播放列表

    * Arguments: `None`

    * Response:
        
        所有播放列表，其信息有:
        * `key`: 播放列表key
        * `name`: 播放列表名
        * `music_list`: 分播放列表中歌曲数

---

### URL: `/api/playlist/<string:key>/`

* Method `GET`: 获取此播放列表中音乐

    * Arguments: 
        * `num`: 获取歌曲数量

    * Response:
        
        返回列表，每个条目为歌曲信息:
        * `key`: 歌曲key
        * `title`: 歌曲名
        * `artist`: 艺术家
        * `album`: 专辑
        * `company`: 唱片公司
        * `public_time`: 出版年份
        * `kbps`: 码率
        * `cover`: 专辑封面URL
        * `audio`: 音频URL
