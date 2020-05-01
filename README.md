# Plotbot

Push matplotlib figures directly to Discord!

To set up, create a file called `auth.toml` in the package directory and put your bot's access token in there like
```
token = 'YOUR_ACCESS_TOKEN'
```
There are additional options such as IP address, port, and temporary directory location in `conf.toml`.

To start the server, simply run `python3 server.py`. You have to add this directory to your Python path as well. To plot something to `server_name`, run
```
import plotbot.client as pb
pb.send_mpl(fig, server_name)
```
where `fig` is a Matplotlib figure object.
