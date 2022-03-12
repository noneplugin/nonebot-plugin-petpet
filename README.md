# nonebot-plugin-petpet

[Nonebot2](https://github.com/nonebot/nonebot2) 插件，制作头像相关的表情包

### 使用

发送“头像表情包”显示下图的列表：

<div align="left">
  <img src="https://s2.loli.net/2022/03/12/d6Biyup8PIHEvNn.jpg" width="400" />
</div>


每个表情包首次使用时会下载对应的图片和字体，可以手动下载 `resources` 下的 `images` 和 `fonts` 文件夹，放置于机器人运行目录下的 `data/petpet/` 文件夹中


#### 触发方式
- 指令 + @user，如： /爬 @小Q
- 指令 + qq号，如：/爬 123456
- 指令 + 自己，如：/爬 自己
- 指令 + 图片，如：/爬 [图片]

前三种触发方式会使用目标qq的头像作为图片

#### 支持的指令

| 指令 | 效果 | 备注 |
| --- | --- | --- |
| 摸<br>摸摸<br>摸头<br>摸摸头<br>rua | <img src="https://s2.loli.net/2022/02/23/oNGVO4iuCk73g8S.gif" width="200" /> | 可使用参数“圆”让头像为圆形<br>如：摸头圆 自己 |
| 亲<br>亲亲 | <img src="https://s2.loli.net/2022/02/23/RuoiqP8plJBgw9K.gif" width="200" /> | 可指定一个或两个目标<br>若为一个则为 发送人 亲 目标<br>若为两个则为 目标1 亲 目标2<br>如：亲 114514 自己 |
| 贴<br>贴贴<br>蹭<br>蹭蹭 | <img src="https://s2.loli.net/2022/02/23/QDCE5YZIfroavub.gif" width="200" /> | 可指定一个或两个目标<br>类似 亲 |
| 顶<br>玩 | <img src="https://s2.loli.net/2022/02/23/YwxA7fFgWyshuZX.gif" width="200" /> |  |
| 拍 | <img src="https://s2.loli.net/2022/02/23/5mv6pFJMNtzHhcl.gif" width="200" /> |  |
| 撕 | <img src="https://s2.loli.net/2022/03/12/eJKIRrpG82LaMoW.jpg" width="200" > | 默认为 发送人 撕 目标<br>可使用参数“滑稽”替换发送人头像为滑稽<br>如：撕滑稽 114514<br>可在图片上添加文本<br>如：撕 拜托你很弱哎 114514 |
| 丢<br>扔 | <img src="https://s2.loli.net/2022/02/23/LlDrSGYdpcqEINu.jpg" width="200" /> |  |
| 抛<br>掷 | <img src="https://s2.loli.net/2022/03/10/W8X6cGZS5VMDOmh.gif" width="200" /> |  |
| 爬 | <img src="https://s2.loli.net/2022/02/23/hfmAToDuF2actC1.jpg" width="200" /> | 默认为随机选取一张爬表情<br>可使用数字指定特定表情<br>如：爬 13 自己 |
| 精神支柱 | <img src="https://s2.loli.net/2022/02/23/WwjNmiz4JXbuE1B.jpg" width="200" /> |  |
| 一直 | <img src="https://s2.loli.net/2022/02/23/dAf9Z3kMDwYcRWv.gif" width="200" /> | 支持gif |
| 加载中 | <img src="https://s2.loli.net/2022/02/23/751Oudrah6gBsWe.gif" width="200" /> | 支持gif |
| 转 | <img src="https://s2.loli.net/2022/02/23/HoZaCcDIRgs784Y.gif" width="200" /> |  |
| 小天使 | <img src="https://s2.loli.net/2022/02/23/ZgD1WSMRxLIymCq.jpg" width="200" /> | 图中名字为目标qq昵称<br>可指定名字，如：小天使 meetwq 自己 |
| 不要靠近 | <img src="https://s2.loli.net/2022/02/23/BTdkAzvhRDLOa3U.jpg" width="200" /> |  |
| 一样 | <img src="https://s2.loli.net/2022/02/23/SwAXoOgfdjP4ecE.jpg" width="200" /> |  |
| 滚 | <img src="https://s2.loli.net/2022/02/23/atzZsSE53UDIlOe.gif" width="200" /> |  |
| 玩游戏<br>来玩游戏 | <img src="https://s2.loli.net/2022/02/23/Xx34I7nT8HjtfKi.png" width="200" /> | 图中描述默认为：来玩休闲游戏啊<br>可指定描述<br>支持gif |
| 膜<br>膜拜 | <img src="https://s2.loli.net/2022/02/23/nPgBJwV5qDb1s9l.gif" width="200" /> |  |
| 吃 | <img src="https://s2.loli.net/2022/02/23/ba8cCtIWEvX9sS1.gif" width="200" /> |  |
| 啃 | <img src="https://s2.loli.net/2022/02/23/k82n76U4KoNwsr3.gif" width="200" /> |  |
| 出警 | <img src="https://s2.loli.net/2022/02/23/3OIxnSZymAfudw2.jpg" width="200" /> |  |
| 警察 | <img src="https://s2.loli.net/2022/03/12/xYLgKVJcd3HvqfM.jpg" width="200" > |  |
| 问问<br>去问问 | <img src="https://s2.loli.net/2022/02/23/GUyax1BF6q5Hvin.jpg" width="200" /> | 名字为qq昵称，可指定名字 |
| 舔<br>舔屏<br>prpr | <img src="https://s2.loli.net/2022/03/05/WMHpwygtmN5bdEV.jpg" width="200" /> | 支持gif |
| 搓 | <img src="https://s2.loli.net/2022/03/09/slRF4ue56xSQzra.gif" width="200" /> |  |
| 墙纸 | <img src="https://s2.loli.net/2022/03/10/tQRXzLamGyWi24s.jpg" width="200" /> | 支持gif |
| 国旗 | <img src="https://s2.loli.net/2022/03/10/p7nwCvgsU3LxBDI.jpg" width="200" /> |  |
| 交个朋友 | <img src="https://s2.loli.net/2022/03/10/SnmkNrjKuFeZvbA.jpg" width="200" /> | 名字为qq昵称，可指定名字 |
| 继续干活 | <img src="https://s2.loli.net/2022/03/12/DnZdAo9IL7q3lXW.jpg" width="200" > |  |
| 完美<br>完美的 | <img src="https://s2.loli.net/2022/03/10/lUS1nmPAKIYtwih.jpg" width="200" /> |  |
| 关注 | <img src="https://s2.loli.net/2022/03/12/FlpjRWCte72ozqs.jpg" width="200" > | 名字为qq昵称，可指定名字 |
| 我朋友说<br>我有个朋友说 | <img src="https://s2.loli.net/2022/03/12/cBk4aG3RwIoYbMF.jpg" width="200" > | 名字为qq昵称，可指定名字<br>如：我朋友说 meetwq 来份涩图 自己 |
| 这像画吗 | <img src="https://s2.loli.net/2022/03/12/PiSAM1T6EvxXWgD.jpg" width="200" > |  |
| 震惊 | <img src="https://s2.loli.net/2022/03/12/4krO6y53bKzYpUg.gif" width="200" > |  |
| 兑换券 | <img src="https://s2.loli.net/2022/03/12/6tS7dDaprb1sUxj.jpg" width="200" > | 默认文字为：qq昵称 + 陪睡券<br>可指定文字 |
