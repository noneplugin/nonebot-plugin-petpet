<div align="center">

  <a href="https://v2.nonebot.dev/">
    <img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot">
  </a>

# nonebot-plugin-petpet

_✨ [Nonebot2](https://github.com/nonebot/nonebot2) 插件，制作头像相关的表情包 ✨_

<p align="center">
  <img src="https://img.shields.io/github/license/noneplugin/nonebot-plugin-petpet" alt="license">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/nonebot-2.0.0rc1+-red.svg" alt="NoneBot">
  <a href="https://pypi.org/project/nonebot-plugin-petpet">
    <img src="https://badgen.net/pypi/v/nonebot-plugin-petpet" alt="pypi">
  </a>
  <a href="https://jq.qq.com/?_wv=1027&k=wDVNrMdr">
    <img src="https://img.shields.io/badge/QQ%E7%BE%A4-682145034-orange" alt="qq group">
  </a>
</p>

</div>


文字类表情包制作：[nonebot-plugin-memes](https://github.com/noneplugin/nonebot-plugin-memes)


### 安装

- 使用 nb-cli

```
nb plugin install nonebot_plugin_petpet
```

- 使用 pip

```
pip install nonebot_plugin_petpet
```

#### 字体和资源

插件使用 [nonebot-plugin-imageutils](https://github.com/noneplugin/nonebot-plugin-imageutils) 插件来绘制文字，字体配置可参考该插件的说明

插件在启动时会检查并下载图片资源，初次使用时需等待资源下载完成

可以手动下载 `resources` 下的 `images` 文件夹，放置于机器人运行目录下的 `data/petpet/` 文件夹中


### 配置项

> 以下配置项可在 `.env.*` 文件中设置，具体参考 [NoneBot 配置方式](https://v2.nonebot.dev/docs/tutorial/configuration#%E9%85%8D%E7%BD%AE%E6%96%B9%E5%BC%8F)

#### `petpet_command_start`
 - 类型：`List[str]`
 - 默认：`[""]`
 - 说明：命令起始标记，默认包含空字符串

#### `petpet_resource_url`
 - 类型：`str`
 - 默认：`https://ghproxy.com/https://raw.githubusercontent.com/noneplugin/nonebot-plugin-petpet/v0.3.x/resources`
 - 说明：资源下载链接，默认为使用`ghproxy`代理的github仓库链接

#### `petpet_disabled_list`
 - 类型：`List[str]`
 - 默认：`[]`
 - 说明：禁用的表情包列表，需填写表情名称的列表，表情名称可以在`data_source.py`文件中查看。若只是临时关闭，可以用下文中的“表情包开关”

#### `petpet_gif_max_size`
 - 类型：`float`
 - 默认：`10`
 - 说明：限制生成的gif的最大体积，单位为`Mb`。若生成的gif体积过大，则先会尝试缩减帧数，其次尝试缩小图片尺寸

#### `petpet_gif_max_frames`
 - 类型：`int`
 - 默认：`100`
 - 说明：限制生成的gif的最大帧数

#### `baidu_trans_appid`
 - 类型：`str`
 - 默认：`""`
 - 说明：百度翻译api相关，可在[百度翻译开放平台](http://api.fanyi.baidu.com)申请

#### `baidu_trans_apikey`
 - 类型：`str`
 - 默认：`""`
 - 说明：百度翻译api相关，可在[百度翻译开放平台](http://api.fanyi.baidu.com)申请

 > “典中典”表情需要设置 `baidu_trans_appid` 和 `baidu_trans_apikey`


### 使用

**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空: `.env.*` 文件中设置 `COMMAND_START=[""]`**

发送“头像表情包”显示下图的列表：

<div align="left">
  <img src="https://s2.loli.net/2023/01/28/wWFVrQh2TmuR7dO.jpg" width="400" />
</div>


#### 触发方式
- 指令 + @user，如： /爬 @小Q
- 指令 + qq号，如：/爬 123456
- 指令 + 自己，如：/爬 自己
- 指令 + 图片，如：/爬 [图片]
- 回复图片消息 + 指令

前三种触发方式会使用目标qq的头像作为图片

回复图片时需要把指令前的“@”删除


#### 随机表情

随机表情 + @user/qq号/自己/图片

如：`随机表情 自己`

会在未禁用的表情中随机选取一个制作表情包


#### 表情包开关

群主 / 管理员 / 超级用户 可以启用或禁用某些表情包

发送 `启用表情/禁用表情 [表情名]`，如：`禁用表情 摸`、`启用表情 petpet 贴 爬`

超级用户 可以设置某个表情包的管控模式（黑名单/白名单）

发送 `全局启用表情 [表情名]` 可将表情设为黑名单模式；

发送 `全局禁用表情 [表情名]` 可将表情设为白名单模式；


#### 支持的指令

<details>
<summary>展开/收起</summary>

| 指令 | 效果 | 备注 |
| --- | --- | --- |
| 万能表情<br>空白表情 | <img src="https://s2.loli.net/2022/05/29/C2VRA6iw4hzWZXO.jpg" width="200" /> | 简单的图片加文字 |
| 摸<br>摸摸<br>摸头<br>摸摸头<br>rua | <img src="https://s2.loli.net/2022/02/23/oNGVO4iuCk73g8S.gif" width="200" /> | 可使用参数“圆”让头像为圆形<br>如：摸头圆 自己 |
| 亲<br>亲亲 | <img src="https://s2.loli.net/2022/02/23/RuoiqP8plJBgw9K.gif" width="200" /> | 可指定一个或两个目标<br>若为一个则为 发送人 亲 目标<br>若为两个则为 目标1 亲 目标2<br>如：亲 114514 自己 |
| 贴<br>贴贴<br>蹭<br>蹭蹭 | <img src="https://s2.loli.net/2022/02/23/QDCE5YZIfroavub.gif" width="200" /> | 可指定一个或两个目标<br>类似 亲 |
| 咖波蹭 | <img src="https://s2.loli.net/2022/11/29/iZpwCVWb5agDKLH.gif" width="200" > |  |
| 顶<br>玩 | <img src="https://s2.loli.net/2022/08/16/WVotKxjqupdCJAS.gif" width="200" /> |  |
| 拍 | <img src="https://s2.loli.net/2022/02/23/5mv6pFJMNtzHhcl.gif" width="200" /> |  |
| 撕 | <img src="https://s2.loli.net/2022/05/29/FDcam9ROPkqvwxH.jpg" width="200" > |  |
| 怒撕 | <img src="https://s2.loli.net/2022/10/11/NepC3ETugIaWnHs.jpg" width="200" > |  |
| 丢<br>扔 | <img src="https://s2.loli.net/2022/02/23/LlDrSGYdpcqEINu.jpg" width="200" /> |  |
| 抛<br>掷 | <img src="https://s2.loli.net/2022/03/10/W8X6cGZS5VMDOmh.gif" width="200" /> |  |
| 爬 | <img src="https://s2.loli.net/2022/02/23/hfmAToDuF2actC1.jpg" width="200" /> | 默认为随机选取一张爬表情<br>可使用数字指定特定表情<br>如：爬 13 自己 |
| 精神支柱 | <img src="https://s2.loli.net/2022/02/23/WwjNmiz4JXbuE1B.jpg" width="200" /> |  |
| 一直 | <img src="https://s2.loli.net/2022/02/23/dAf9Z3kMDwYcRWv.gif" width="200" /> | 支持gif |
| 一直一直 | <img src="https://s2.loli.net/2022/10/15/hn5Q4jm29pXNsrL.gif" width="200" /> | 支持gif |
| 加载中 | <img src="https://s2.loli.net/2022/02/23/751Oudrah6gBsWe.gif" width="200" /> | 支持gif |
| 转 | <img src="https://s2.loli.net/2022/02/23/HoZaCcDIRgs784Y.gif" width="200" /> |  |
| 风车转 | <img src="https://s2.loli.net/2022/12/17/7x8DHoYWnCBTeqL.gif" width="200" > |  |
| 小天使 | <img src="https://s2.loli.net/2022/02/23/ZgD1WSMRxLIymCq.jpg" width="200" /> | 图中名字为目标qq昵称<br>可指定名字，如：小天使 meetwq 自己 |
| 不要靠近 | <img src="https://s2.loli.net/2022/02/23/BTdkAzvhRDLOa3U.jpg" width="200" /> |  |
| 一样 | <img src="https://s2.loli.net/2022/02/23/SwAXoOgfdjP4ecE.jpg" width="200" /> |  |
| 滚 | <img src="https://s2.loli.net/2022/02/23/atzZsSE53UDIlOe.gif" width="200" /> |  |
| 玩游戏<br>来玩游戏 | <img src="https://s2.loli.net/2022/05/31/j9ZKB7cFOSklzMe.jpg" width="200" /> | 图中描述默认为：来玩休闲游戏啊<br>可指定描述<br>支持gif |
| 膜<br>膜拜 | <img src="https://s2.loli.net/2022/02/23/nPgBJwV5qDb1s9l.gif" width="200" /> |  |
| 吃 | <img src="https://s2.loli.net/2022/02/23/ba8cCtIWEvX9sS1.gif" width="200" /> |  |
| 可莉吃 | <img src="https://s2.loli.net/2022/11/29/R12XlsdTjCYqnBh.gif" width="200" /> |  |
| 啃 | <img src="https://s2.loli.net/2022/02/23/k82n76U4KoNwsr3.gif" width="200" /> |  |
| 胡桃啃 | <img src="https://s2.loli.net/2022/11/29/JUCbMuxgpYDfAWo.gif" width="200" /> |  |
| 出警 | <img src="https://s2.loli.net/2022/05/31/Q7WL1q2TlHgnERr.jpg" width="200" /> |  |
| 警察 | <img src="https://s2.loli.net/2022/03/12/xYLgKVJcd3HvqfM.jpg" width="200" > |  |
| 问问<br>去问问 | <img src="https://s2.loli.net/2022/02/23/GUyax1BF6q5Hvin.jpg" width="200" /> | 名字为qq昵称，可指定名字 |
| 舔<br>舔屏<br>prpr | <img src="https://s2.loli.net/2022/03/05/WMHpwygtmN5bdEV.jpg" width="200" /> | 支持gif |
| 搓 | <img src="https://s2.loli.net/2022/03/09/slRF4ue56xSQzra.gif" width="200" /> |  |
| 墙纸 | <img src="https://s2.loli.net/2022/10/01/wm3pFvEZeUctA4J.gif" width="200" /> |  |
| 国旗 | <img src="https://s2.loli.net/2022/03/10/p7nwCvgsU3LxBDI.jpg" width="200" /> |  |
| 交个朋友 | <img src="https://s2.loli.net/2022/03/10/SnmkNrjKuFeZvbA.jpg" width="200" /> | 名字为qq昵称，可指定名字 |
| 继续干活<br>打工人 | <img src="https://s2.loli.net/2022/04/20/LIak2BsJ9Dd5O7l.jpg" width="200" > |  |
| 完美<br>完美的 | <img src="https://s2.loli.net/2022/03/10/lUS1nmPAKIYtwih.jpg" width="200" /> |  |
| 关注 | <img src="https://s2.loli.net/2022/03/12/FlpjRWCte72ozqs.jpg" width="200" > | 名字为qq昵称，可指定名字 |
| 我朋友说<br>我有个朋友说 | <img src="https://s2.loli.net/2022/03/12/cBk4aG3RwIoYbMF.jpg" width="200" > | 没有图片则使用发送者的头像<br>可指定名字<br>如“我朋友张三说 来份涩图” |
| 这像画吗 | <img src="https://s2.loli.net/2022/03/12/PiSAM1T6EvxXWgD.jpg" width="200" > |  |
| 震惊 | <img src="https://s2.loli.net/2022/03/12/4krO6y53bKzYpUg.gif" width="200" > |  |
| 兑换券 | <img src="https://s2.loli.net/2022/03/12/6tS7dDaprb1sUxj.jpg" width="200" > | 默认文字为：qq昵称 + 陪睡券<br>可指定文字 |
| 听音乐 | <img src="https://s2.loli.net/2022/03/15/rjgvbXeOJtIW8fF.gif" width="200" > |  |
| 典中典 | <img src="https://s2.loli.net/2022/03/18/ikQ1IB6hS4x3EjD.jpg" width="200" > |  |
| 哈哈镜 | <img src="https://s2.loli.net/2022/03/15/DwRPaErSNZWXGgp.gif" width="200" > |  |
| 永远爱你 | <img src="https://s2.loli.net/2022/03/15/o6mhWk7crwdepU5.gif" width="200" > |  |
| 对称 | <img src="https://s2.loli.net/2022/03/15/HXntCy8kc7IRZxp.jpg" width="200" > | 可使用参数“上”、“下”、“左”、“右”指定对称方向<br>支持gif |
| 安全感 | <img src="https://s2.loli.net/2022/03/15/58pPzrgxJNkUYRT.jpg" width="200" > | 可指定描述 |
| 永远喜欢<br>我永远喜欢 | <img src="https://s2.loli.net/2022/03/15/EpTiUbcoVGCXLkJ.jpg" width="200" > | 图中名字为目标qq昵称<br>可指定名字<br>可指定多个目标叠buff |
| 采访 | <img src="https://s2.loli.net/2022/03/15/AYpkWEc2BrXhKeU.jpg" width="200" > | 可指定描述 |
| 打拳 | <img src="https://s2.loli.net/2022/03/18/heA9fCPMQWXBxTn.gif" width="200" > |  |
| 群青 | <img src="https://s2.loli.net/2022/03/18/drwXx3yK14IMVCf.jpg" width="200" > |  |
| 捣 | <img src="https://s2.loli.net/2022/03/30/M9xUehlV64OpGoY.gif" width="200" > |  |
| 捶 | <img src="https://s2.loli.net/2022/03/30/ElnARr7ohVXjtJx.gif" width="200" > |  |
| 需要<br>你可能需要 | <img src="https://s2.loli.net/2022/03/30/VBDG74QeZUYcunh.jpg" width="200" > |  |
| 捂脸 | <img src="https://s2.loli.net/2022/03/30/NLy4Eb6CHKP3Svo.jpg" width="200" > |  |
| 敲 | <img src="https://s2.loli.net/2022/04/14/uHP8z3bDMtGdOCk.gif" width="200" > |  |
| 垃圾<br>垃圾桶 | <img src="https://s2.loli.net/2022/04/14/i1ok2NUYaMfKezT.gif" width="200" > |  |
| 为什么@我<br>为什么at我 | <img src="https://s2.loli.net/2022/04/14/qQYydurABV7TMbN.jpg" width="200" > |  |
| 像样的亲亲 | <img src="https://s2.loli.net/2022/04/14/1KvLjb2uRYQ9mCI.jpg" width="200" > |  |
| 啾啾 | <img src="https://s2.loli.net/2022/04/20/v3YrbLMnND8BoPK.gif" width="200" > |  |
| 吸<br>嗦 | <img src="https://s2.loli.net/2022/04/20/LlFNscXC1IQrkgE.gif" width="200" > |  |
| 锤 | <img src="https://s2.loli.net/2022/04/20/ajXFm95tHRM6CzZ.gif" width="200" > |  |
| 紧贴<br>紧紧贴着 | <img src="https://s2.loli.net/2022/04/20/FiBwc3ZxvVLObGP.gif" width="200" > |  |
| 注意力涣散 | <img src="https://s2.loli.net/2022/05/11/mEtyxoZ3DfwBCn5.jpg" width="200" > |  |
| 阿尼亚喜欢 | <img src="https://s2.loli.net/2022/08/16/PNCZxzqvV9uDFEf.jpg" width="200" > | 支持gif |
| 想什么 | <img src="https://s2.loli.net/2022/05/18/ck1jNO2K8Qd6Lo3.jpg" width="200" > | 支持gif |
| 远离 | <img src="https://s2.loli.net/2022/05/31/lqyOu25WPTsGBcb.jpg" width="200" > | 可指定多个目标 |
| 结婚申请<br>结婚登记 | <img src="https://s2.loli.net/2022/05/31/tZR3ls7cBrdGHTL.jpg" width="200" > |  |
| 离婚协议<br>离婚申请 | <img src="https://s2.loli.net/2023/01/08/XHakWIShp7q1CjR.jpg" width="200" > |  |
| 小画家 | <img src="https://s2.loli.net/2022/06/23/KCD73EbgqzWFxr4.jpg" width="200" > |  |
| 复读 | <img src="https://s2.loli.net/2022/08/16/E6vgRCt3MSLfAWU.gif" width="200" > | 复读内容默认为“救命啊”<br>可指定多个目标 |
| 防诱拐 | <img src="https://s2.loli.net/2022/07/21/ve6lcYaiV4wfhHg.jpg" width="200" > |  |
| 字符画 | <img src="https://s2.loli.net/2022/07/21/R58eG7mVZWPp1Cy.jpg" width="200" > | 支持gif |
| 我老婆 | <img src="https://s2.loli.net/2022/08/16/7wPht5rp6sk1ZCq.jpg" width="200" > |  |
| 胡桃平板 | <img src="https://s2.loli.net/2022/08/16/Mc5HvfB6ywqLQiV.jpg" width="200" > | 支持gif |
| 胡桃放大 | <img src="https://s2.loli.net/2022/10/01/ISotJVp1xOfgvlq.gif" width="200" > | 支持gif |
| 讲课<br>敲黑板 | <img src="https://s2.loli.net/2022/08/16/VpdIHsteKocgRzP.jpg" width="200" > | 支持gif |
| 上瘾<br>毒瘾发作 | <img src="https://s2.loli.net/2022/08/26/WAVDFfJB7tH5z3y.jpg" width="200" > | 支持gif |
| 手枪 | <img src="https://s2.loli.net/2022/08/26/MRO3mqvfbaxkB1t.jpg" width="200" > |  |
| 高血压 | <img src="https://s2.loli.net/2022/08/26/9qbyN2h38MAkRZE.jpg" width="200" > | 支持gif |
| 看书 | <img src="https://s2.loli.net/2022/08/26/SeAC86RgDlUvLNY.jpg" width="200" > |  |
| 遇到困难请拨打 | <img src="https://s2.loli.net/2022/08/26/KWGSf6qErB14uwp.jpg" width="200" > | 可指定一个或两个目标 |
| 迷惑 | <img src="https://s2.loli.net/2022/10/01/WqfAXNpD8JkVnUH.gif" width="200" > | 支持gif |
| 打穿<br>打穿屏幕 | <img src="https://s2.loli.net/2022/10/01/ndxBbC1TKeRYv9X.gif" width="200" > | 支持gif |
| 击剑<br>🤺 | <img src="https://s2.loli.net/2022/10/01/97uZYdFs16CkJhQ.gif" width="200" > |  |
| 抱大腿 | <img src="https://s2.loli.net/2022/10/01/mivPkLle6qwZQsg.gif" width="200" > |  |
| 唐可可举牌 | <img src="https://s2.loli.net/2022/10/01/LdGk9MmzYaebFt5.gif" width="200" > |  |
| 无响应 | <img src="https://s2.loli.net/2022/10/01/vjXnOgcSVLGfdCQ.jpg" width="200" > |  |
| 抱紧 | <img src="https://s2.loli.net/2022/10/01/vYgl3nRmXuGwqDd.jpg" width="200" > |  |
| 看扁 | <img src="https://s2.loli.net/2022/10/08/kAHs6GYnmRh28WB.jpg" width="200" > | 支持gif<br>可指定描述<br>可指定缩放倍率，默认为2<br>如：看扁 3 自己 |
| 看图标 | <img src="https://s2.loli.net/2022/10/08/Ek8Vu6eFyQKJnos.jpg" width="200" > | 支持gif<br>可指定描述 |
| 舰长 | <img src="https://s2.loli.net/2022/10/11/8kPgVo6yzWMhfqU.jpg" width="200" > | 可指定1~5个目标 |
| 急急国王 | <img src="https://s2.loli.net/2022/10/11/RqFP8Gtr2CQmSTU.jpg" width="200" > | 可指定方块中的字和描述<br>可用多个图片替代方块 |
| 不文明 | <img src="https://s2.loli.net/2022/10/15/XBqrksgCcAx1YaH.jpg" width="200" > |  |
| 一起 | <img src="https://s2.loli.net/2022/10/15/Ujt7avy9d5TfOlW.jpg" width="200" > |  |
| 波纹 | <img src="https://s2.loli.net/2022/11/09/hTnrF1e5gaYbxsX.gif" width="200" > | 支持gif |
| 诈尸<br>秽土转生 | <img src="https://s2.loli.net/2022/11/09/z2alEPjdsrNSyMU.gif" width="200" > |  |
| 卡比锤<br>卡比重锤 | <img src="https://s2.loli.net/2022/11/09/ouF5MxzQaqjC64d.gif" width="200" > | 支持gif<br>可使用参数“圆”让头像为圆形 |
| 木鱼 | <img src="https://s2.loli.net/2022/11/29/fuen9axo2d67bRE.gif" width="200" > |  |
| 凯露指 | <img src="https://s2.loli.net/2022/11/29/8fjBb1rCe6oIdRY.png" width="200" > |  |
| 踢球 | <img src="https://s2.loli.net/2022/11/29/o9zns8YvZLguV6G.gif" width="200" > |  |
| 砸 | <img src="https://s2.loli.net/2022/11/29/fTqa5V1dArhxDHX.jpg" width="200" > | 支持gif |
| 波奇手稿 | <img src="https://s2.loli.net/2022/11/29/Aw8HsGud7JoMKqW.gif" width="200" > |  |
| 坐得住<br>坐的住 | <img src="https://s2.loli.net/2022/12/03/gaQsO6AkVtPF3CW.jpg" width="200" > | 图中名字为目标qq昵称<br>可自定义名字 |
| 偷学 | <img src="https://s2.loli.net/2022/12/17/v6C9jegrNy1AJRu.jpg" width="200" > | 描述默认为“偷学群友数理基础”<br>可自定义描述 |
| 恍惚 | <img src="https://s2.loli.net/2022/12/17/fU6i7tr8egbxaMI.jpg" width="200" > |  |
| 恐龙<br>小恐龙 | <img src="https://s2.loli.net/2023/01/08/hWaoIZ4JxDgX9FA.jpg" width="200" > | 支持gif |
| 挠头 | <img src="https://s2.loli.net/2023/01/08/DeuAJSQRdrC2v51.gif" width="200" > |  |
| 鼓掌 | <img src="https://s2.loli.net/2023/01/08/SGhsngjWQLRemPd.gif" width="200" > |  |
| 追列车<br>追火车 | <img src="https://s2.loli.net/2023/01/08/NJ1FnKkdcrDBtEx.gif" width="200" > |  |
| 万花筒<br>万花镜 | <img src="https://s2.loli.net/2023/01/08/obSnWmDOiFcqYkN.jpg" width="200" > | 支持gif<br>可使用参数“圆”让头像为圆形 |
| 加班 | <img src="https://s2.loli.net/2023/01/08/LTcqjGobDkSVQIN.jpg" width="200" > |  |
| 头像公式<br>等价无穷小 | <img src="https://s2.loli.net/2023/01/28/7CQWSZieyXm5THY.jpg" width="200" > |  |
| 土豆 | <img src="https://s2.loli.net/2023/01/28/5PAfjsgwBdNzlbn.jpg" width="200" > |  |
| 打印 | <img src="https://s2.loli.net/2023/01/28/s9F5Ar6QKOqLtBi.gif" width="200" > |  |

</details>


### 特别感谢

- [FloatTech/ZeroBot-Plugin](https://github.com/FloatTech/ZeroBot-Plugin) 基于 ZeroBot 的 OneBot 插件
- [Dituon/petpet](https://github.com/Dituon/petpet) Mirai插件 生成各种奇怪的图片
