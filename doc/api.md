# 注意

请调用本API的所有app将自己的`User-Agent`设置为`应用名:版本号:联系方式`的形式，例如`MyApp:0.1:admin@doufm.info`，方便进行管理。

# 用户权限

用户总共分为3个权限，分别为

* `disable`: 禁用
* `normal`: 普通用户
* `admin`: 管理员

采用对应权限的账号登陆后会通过cookie识别用户权限。

# API 文档

## music API

### URL: `/api/music/`

* Method `GET`: 搜索歌曲

    * level: None

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

### URL: `/api/music/<string:key>/`

* Method `PATCH`: 修改歌曲信息

    * level: `admin`

    * Arguments: 
        * `title`: 歌曲名
        * `artist`: 艺术家
        * `album`: 专辑
        * `company`: 唱片公司
        * `public_time`: 出版年份

    * Response:
        
        返回歌曲信息:
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

* Method `DELETE`: 删除歌曲

    * level: `admin`
    * Arguments: `None`
    * Response: `None`


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

### URL: `/api/channel/<string:key>/`

* Method `PATCH`: 修改列表信息

    * level: `admin`

    * Arguments: 
        * `name`: 列表名
        * `update_num`: 每日更新数量
        * `playable`: 是否显示在播放列表中

    * Response:
        
        返回歌曲信息:
        * `key`: 分类key
        * `name`: 分类名
        * `music_list`: 分类中歌曲数
        * `update_num`: 本分类每日更新数量
        * `playable`: 是否显示在播放列表中
        * `upload_date`: 分类创建时间时间

* Method `DELETE`: 删除分类

    * level: `admin`
    * Arguments: `None`
    * Response: `None`

## user API

### URL: `/api/user/`

* Method `GET`: 获取用户列表

    * level: `admin`

    * Arguments: 
        * `key`: 用户key
        * `name`: 用户名
        * `level`: 权限
        * `start`, `end`: 起始, 终止

    * Response:
        
        用户列表，其中每一条目为一个列表，列表信息:
        * `key`: 用户key
        * `name`: 用户名
        * `level`: 权限
        * `regist_date`: 注册时间
        * `listened`: 听过歌曲数
        * `favor`: 喜欢歌曲数
        * `dislike`: 讨厌歌曲数

    * Notes:
        * 当参数为空时，返回概述：
            * `/api/user/`:
                ```
                {
                    "count": 10
                }
                ```
        * 条件查询
            * `/api/user/?name=name1`: 搜索用户名为title1的用户
        * 使用参数`start`, `end`按范围查询歌曲
            * `/api/user/?start=0&end=2`: 获取前两个用户
            * `/api/user/?start=0`: 获取全部用户

* Method `POST`: 用户注册

    * level: None

    * Arguments: 
        * `name`: 用户名
        * `password`: 密码

    * Response:

        若注册失败返回None，否则返回用户信息:
        * `key`: 用户key
        * `name`: 用户名
        * `level`: 权限
        * `regist_date`: 注册时间
        * `listened`: 听过歌曲数
        * `favor`: 喜欢歌曲数
        * `dislike`: 不喜欢歌曲数

---

### URL: `/api/user/current/`

* Method `GET`: 获取当前登录用户信息

    * level: None

    * Arguments: None

    * Response:

        若未登录返回None，否则返回用户信息:
        * `key`: 用户key
        * `name`: 用户名
        * `level`: 权限
        * `regist_date`: 注册时间
        * `favor`: 喜欢歌曲数
        * `listened`: 听过歌曲数
        * `skipped`: 跳过歌曲数
        * `dislike`: 不喜欢歌曲数

* Method `POST`: 用户登录

    * level: None

    * Arguments: 
        * `name`: 用户名
        * `password`: 密码
 
    * Response:

        若登录失败返回None，否则返回用户信息:
        * `key`: 用户key
        * `name`: 用户名
        * `level`: 权限
        * `regist_date`: 注册时间
        * `favor`: 喜欢歌曲数
        * `dislike`: 不喜欢歌曲数
        * `listened`: 听过歌曲数


* Method `DELETE`: 用户登出

    * level: None
    * Arguments: None
    * Response: None

---

### URL: `/api/user/<string:key>/`

* Method `PATCH`: 修改用户信息

    * level: `admin`

    * Arguments: 
        * `password`: 密码
        * `level`: 权限('disable', 'normal', 'admin')

    * Response:
        
        返回用户信息:
        * `key`: 用户key
        * `name`: 用户名
        * `level`: 权限
        * `regist_date`: 注册时间
        * `favor`: 喜欢歌曲数
        * `dislike`: 不喜欢歌曲数
        * `listened`: 听过歌曲数

* Method `DELETE`: 删除用户

    * level: `admin`
    * Arguments: `None`
    * Response: `None`

---

### URL: `/api/user/current/history/`

* Method `GET`: 获取用户操作日志

    * level: `normal`, `admin`

    * Arguments: 
        * `start`: 起始
        * `end`: 终止

    * Response:
        
        返回操作信息列表，内容包括:
        * `date`: 操作事件
        * `op`: 操作类型
        * `key`: 音乐key
        * `title`: 音乐标题
        * `cover`: 封面地址

* Method `POST`: 添加用户操作

    * level: `normal`, `admin`

    * Arguments:
        * `op`: 操作类型（`favor`, `dislike`, `shared`, `listened`）
        * `key`: 音乐key

    * Response: `None`

---

### URL: `/api/user/current/favor/`

* Method `GET`: 获取用户喜欢列表

    * level: `normal`, `admin`

    * Arguments: 
        * `start`: 起始
        * `end`: 终止

    * Response:
        
        返回喜欢歌曲列表，内容包括:
        * `key`: 歌曲key
        * `title`: 歌曲名
        * `artist`: 艺术家
        * `album`: 专辑
        * `company`: 唱片公司
        * `public_time`: 出版年份
        * `kbps`: 码率
        * `cover`: 专辑封面URL
        * `audio`: 音频URL

## playlist API

### URL: `/api/playlist/`

* Method `GET`: 获取播放列表

    * level: None

    * Arguments: `None`

    * Response:
        
        所有播放列表，其信息有:
        * `key`: 播放列表key
        * `name`: 播放列表名
        * `music_list`: 分播放列表中歌曲数

---

### URL: `/api/playlist/<string:key>/`

* Method `GET`: 获取此播放列表中音乐

    * level: None

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
