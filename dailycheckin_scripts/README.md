# 配置说明

## 参数说明

### Web 签到配置

|            Name            |                        归属                         | 属性 | 说明                                                         |
| :------------------------: | :-------------------------------------------------: | :--: | :----------------------------------------------------------- |
|     _**IQIYI**_.cookie     |          [爱奇艺](https://www.iqiyi.com/)           | Web  | 爱奇艺 帐号的 cookie 信息                                    |
|     _**KGQQ**_.cookie      |     [全民K歌](https://kg.qq.com/index-pc.html)      | Web  | 全民K歌 帐号的 cookie 信息                                   |
|   _**VQQ**_.auth_refresh   |            [腾讯视频](https://v.qq.com/)            | Web  | 腾讯视频 搜索 带有 `auth_refresh` 的 url，填写其完整的 URL   |
|      _**VQQ**_.cookie      |            [腾讯视频](https://v.qq.com/)            | Web  | 腾讯视频 搜索 带有 `auth_refresh` 的 url，填写其对应的 cookie |
|    _**YOUDAO**_.cookie     |     [有道云笔记](https://note.youdao.com/web/)      | Web  | 有道云笔记 帐号的 cookie 信息                                |
|    _**MUSIC163**_.phone    |        [网易云音乐](https://music.163.com/)         | 账号 | 网易云音乐 帐号的手机号                                      |
|  _**MUSIC163**_.password   |        [网易云音乐](https://music.163.com/)         | 账号 | 网易云音乐 帐号的密码                                        |
|  _**ONEPLUSBBS**_.cookie   | [一加手机社区官方论坛](https://www.oneplusbbs.com/) | Web  | 一加手机社区官方论坛 账户的 cookie                           |
|     _**TIEBA**_.cookie     |   [百度贴吧](https://tieba.baidu.com/index.html)    | Web  | 百度贴吧 cookie                                              |
|   _**BILIBILI**_.cookie    |        [Bilibili](https://www.bilibili.com)         | Web  | Bilibili cookie                                              |
|  _**BILIBILI**_.coin_num   |        [Bilibili](https://www.bilibili.com)         | Web  | Bilibili 每日投币数量                                        |
|  _**BILIBILI**_.coin_type  |        [Bilibili](https://www.bilibili.com)         | Web  | Bilibili 投币方式 默认为 0 ；1: 为关注用户列表视频投币 0: 为随机投币。如果关注用户发布的视频不足配置的投币数，则剩余部分使用随机投币 |
| _**BILIBILI**_.silver2coin |        [Bilibili](https://www.bilibili.com)         | Web  | Bilibili 是否开启银瓜子换硬币，默认为 True 开启              |
|     _**V2EX**_.cookie      |            [V2EX](https://www.v2ex.com/)            | Web  | V2EX 每日签到                                                |
|      _**V2EX**_.proxy      |            [V2EX](https://www.v2ex.com/)            | Web  | V2EX 代理的信息，无密码例子: http://127.0.0.1:1080 有密码例子: http://username:password@127.0.0.1:1080 |
|    _**WWW2NZZ**_.cookie    |          [咔叽网单](https://www.2nzz.com/)          | Web  | 咔叽网单 每日签到                                            |
|     _**SMZDM**_.cookie     |         [什么值得买](https://www.smzdm.com)         | Web  | 什么值得买 每日签到                                          |
|    _**CLOUD189**_.phone    |          [天翼云盘](https://cloud.189.cn/)          | Web  | 天翼云盘 手机号                                              |
|  _**CLOUD189**_.password   |          [天翼云盘](https://cloud.189.cn/)          | Web  | 天翼云盘 手机号对应的密码                                    |
|     _**POJIE**_.cookie     |    [吾爱破解](https://www.52pojie.cn/index.php)     | Web  | 吾爱破解 cookie                                              |
|     _**MEIZU**_.cookie     |         [MEIZU 社区](https://bbs.meizu.cn)          | Web  | MEIZU 社区 cookie                                            |
|   _**MEIZU**_.draw_count   |         [MEIZU 社区](https://bbs.meizu.cn)          | Web  | MEIZU 社区 抽奖次数                                          |
|    _**ZHIYOO**_.cookie     |           [智友邦](http://zhizhiyoo.net/)           | Web  | 智友邦 WEB Cookie                                            |
|     _**CSDN**_.cookie      |            [CSDN](https://www.csdn.net/)            | Web  | CSDN Cookie                                                  |
|   _**EVERPHOTO**_.mobile   |        [时光相册](https://web.everphoto.cn/)        | Web  | 时光相册 https://web.everphoto.cn/api/auth URL 表单内的 mobile 数据 |
|  _**EVERPHOTO**_.password  |        [时光相册](https://web.everphoto.cn/)        | Web  | 时光相册 https://web.everphoto.cn/api/auth URL 表单内的 password 数据 |

### 公众号签到配置

|           Name           |    归属    |  属性  | 说明                                                         |
| :----------------------: | :--------: | :----: | :----------------------------------------------------------- |
|     _**WOMAIL**_.url     | 联通沃邮箱 | 公众号 | 联通沃邮箱 公众号 `https://nyan.mail.wo.cn/cn/sign/index/index?mobile` 开头的 URL |
| _**WOMAIL**_.pause21days | 联通沃邮箱 | 公众号 | true: 开启21天自动暂停，false: 关闭自动暂停，每天都签到。默认开启自动暂停 |
|    _**WOMAIL**_.phone    | 联通沃邮箱 | 公众号 | 手机号                                                       |
|  _**WOMAIL**_.password   | 联通沃邮箱 | 公众号 | 密码                                                         |

### APP 签到配置

|           Name           |                 归属                  | 属性 | 说明                                                         |
| :----------------------: | :-----------------------------------: | :--: | :----------------------------------------------------------- |
|    _**FMAPP**_.token     |                Fa米家                 | APP  | Fa米家 APP headers 中的 token                                |
|    _**FMAPP**_.cookie    |                Fa米家                 | APP  | Fa米家 APP headers 中的 cookie                               |
|   _**FMAPP**_.blackbox   |                Fa米家                 | APP  | Fa米家 APP headers 中的 blackBox                             |
|  _**FMAPP**_.device_id   |                Fa米家                 | APP  | Fa米家 APP headers 中的 deviceId                             |
|  _**FMAPP**_.fmversion   |                Fa米家                 | APP  | Fa米家 APP headers 中的 fmVersion                            |
|      _**FMAPP**_.os      |                Fa米家                 | APP  | Fa米家 APP headers 中的 os                                   |
|  _**FMAPP**_.useragent   |                Fa米家                 | APP  | Fa米家 APP headers 中的 User-Agent                           |
|    _**ACFUN**_.phone     |    [AcFun](https://www.acfun.cn/)     | APP  | AcFun 手机账号                                               |
|   _**ACFUN**_.password   |    [AcFun](https://www.acfun.cn/)     | APP  | AcFun 账号密码                                               |
|    _**MGTV**_.params     |                芒果 TV                | APP  | 芒果 TV 请求参数                                             |
|  _**PICACOMIC**_.email   | [哔咔漫画](https://www.picacomic.com) | APP  | 哔咔漫画 账号                                                |
| _**PICACOMIC**_.password | [哔咔漫画](https://www.picacomic.com) | APP  | 哔咔漫画 密码                                                |
|     _**WEIBO**_.url      |                 微博                  | APP  | 抓取开头为 `https://api.weibo.cn/2/users/show?` 的整个 url 填入即可 |
|   _**DUOKAN**_.cookie    |               多看阅读                | APP  | 多看阅读 cookie， 抓取开头为 `https://www.duokan.com` 下的 cookie 即可 |
|     _**WZYD**_.data      |               王者营地                | APP  | 王者营地 请求体中的 data， 抓包 APP 中域名为 `https://ssl.kohsocial.qq.com` 请求内容的全部参数 |
|   _**HEYTAP**_.cookie    |               欢太商城                | APP  | 欢太商城 请求体中的 Cookie， 抓包 APP 中域名为 `https://store.oppo.com/` 请求内容的 Cookie |
|  _**HEYTAP**_.useragent  |               欢太商城                | APP  | 欢太商城 请求体中的 User-Agent， 抓包 APP 中域名为 `https://store.oppo.com/` 请求内容的 User-Agent |
|    _**HEYTAP**_.draw     |               欢太商城                | APP  | 是否开启抽奖，默认 false                                     |
|   _**UNICOM**_.mobile    |              联通营业厅               | APP  | 联通营业厅 手机号                                            |
|  _**UNICOM**_.password   |              联通营业厅               | APP  | 联通营业厅 6位登录密码                                       |
|   _**UNICOM**_.app_id    |              联通营业厅               | APP  | 联通营业厅 请求体中的 appId， 抓包 APP 中域名为 `https://m.client.10010.com/mobileService/login.htm` 请求内容的 appId |

### 其他任务配置

|          Name           |                           归属                            | 属性 | 说明                                    |
| :---------------------: | :-------------------------------------------------------: | :--: | :-------------------------------------- |
|  _**MIMOTION**_.phone   |                         小米运动                          | 其他 | 小米运动刷步数的手机账号                |
| _**MIMOTION**_.password |                         小米运动                          | 其他 | 小米运动刷步数的手机账号密码            |
| _**MIMOTION**_.min_step |                         小米运动                          | 其他 | 小米运动刷步数的最小步数                |
| _**MIMOTION**_.max_step |                         小米运动                          | 其他 | 小米运动刷步数的最大步数                |
|  _**BAIDUT**_.data_url  | [百度搜索资源平台](https://ziyuan.baidu.com/site/index#/) | 其他 | 提交网站的 URL 链接                     |
| _**BAIDUT**_.submit_url | [百度搜索资源平台](https://ziyuan.baidu.com/site/index#/) | 其他 | 百度搜索资源平台 提交百度网站的目标 URL |
|   _**BAIDUT**_.times    | [百度搜索资源平台](https://ziyuan.baidu.com/site/index#/) | 其他 | 每日对同一个网站提交次数                |
