import requests as r
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
import asyncio
import os

TOKEN = os.environ.get('TELEGRAM_TOKEN')
user_id = os.environ.get('TELEGRAM_USER_ID')

MONTHS_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

def format_message(month: int, datas_disponiveis: list | None) -> str:
    today = datetime.now().strftime("%d/%m/%Y")
    month_name = MONTHS_PT[month]

    header = (
        f"🔍 *Resultado da busca*\n"
        f"Salvador\-BA ➡️ Petrolina\-PE\n"
        f"\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\n"
        f"📅 Mês pesquisado: *{month_name}/{2026}*\n"
        f"🗓 Busca realizada em: {today}\n"
        f"\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\n"
    )

    if datas_disponiveis:
        links = "\n".join(
            f"[🎫 Comprar passagem](https://www.aguiabranca.com.br/onibus/salvador-ba/petrolina-pe?Ida={dia.split('/')[0]}-{month}-2026&crianca=0&freeTicketType=5&bebe=0&adulto=1) — 🗓 {dia}"
            for dia in datas_disponiveis
        )
        body = f"✅ *Passagens encontradas:*\n\n{links}"
    else:
        body = f"❌ Nenhuma passagem encontrada para o mês de {month_name}/{2026}\."

    return header + body

def find_tickets(month):

    datas_disponiveis = []

    print(f'Iniciando busca para o mes {month:02d}...')
    for i in range(1,32):
        response = r.get(f'https://www.aguiabranca.com.br/onibus/salvador-ba/petrolina-pe?Ida={i}-{month}-2026&crianca=0&freeTicketType=5&bebe=0&adulto=1')
        if 'data-sufficient="true"' in str(response.content):
            datas_disponiveis.append(f'{i:02d}/{month:02d}')

    if len(datas_disponiveis) > 0:
        print(f'passagens encontradas: {datas_disponiveis}')
        return datas_disponiveis
    else:
        print('Nenhuma passagem encontrada')
        return None
    
# Function to handle the /start command
async def start():
    bot = Bot(token=TOKEN)
    async with bot:
        await bot.send_message(chat_id=user_id, text='teste')
    month = 11  # ou receba dinamicamente
    datas = find_tickets(month)
    message = format_message(month, datas)
    async with bot:
        await bot.send_message(chat_id=user_id, text=message, parse_mode="MarkdownV2", disable_web_page_preview=True)
    # await update.message.reply_text(
    #     message,
    #     parse_mode="MarkdownV2",
    #     disable_web_page_preview=True
    # )
    
if __name__ == '__main__':
    asyncio.run(start())
