# Style Configuration File

The style file options were added with the update to version 0.8 and offer a variety of ways to style the lyrics in the default mode.
<br></br>
<div align="center">
<img width="500" src="https://github.com/user-attachments/assets/53ed773f-b398-43b8-99d5-f212fdcca540"/>
</div>
<br></br>

There are two options available for each section – color and font style. By default, the configuration file is stored in `src/style.config` and is loaded automatically at every startup except the argument `-s, --style` has not been passed. The configuration file looks like this:

```
[DEFAULT]

passed_color: #6c6c6c, normal
highlight_color: #00ff00
future_color: #ffffff, normal
```

Colors must be provided as hex values, while font styles are defined as strings. These font styles are supported:

| <center>font-style</center>  | <center>example</center>  |
| ------------| ---------|
| normal      | Hello World !
| bold        | **Hello World !**
| italic      | *Hello World !*
| underline   | <ins>Hello World !</ins>
| cross_out | ~~Hello World !~~ 

A different configuration file can be applied by using the `-s, --style` argument.