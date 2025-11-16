# Mario Kart Wii Challenge Bot

A Discord bot for creating Mario Kart Wii challenges.

## Features

- Create challenge messages with a specific format
- Submit and get the time of .rkg files

## How to use

1. Clone the repository

```bash
git clone https://github.com/TheDoubleMix/mkw-challenge-bot.git
cd mkw-challenge-bot
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a  `.env` file and add your discord bot's token to it:

```
DISCORD_BOT_TOKEN=<insert bot token here>
```

4. Copy `config.example.json` to `config.json`:

```bash
cp config.example.json config.json
```
Then edit `config.json` with your server's

- challenge channel ID
- submit channel ID
- challenge staff role ID
- starting challenge number

5. Run `main.py`

```bash
python main.py
```

## Discord Bot Permissions

When inviting the bot, enable these

### OAuth2 Scopes:

- `bot`
- `applications.commands`

### Bot Permissions:

- `View Channels`
- `Send Messages`
- `Use Slash Commands`

## License

This project uses the MIT License