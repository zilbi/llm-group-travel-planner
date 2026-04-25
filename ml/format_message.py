from ml.links_search import build_travel_links

async def format_message(trip,data_prev,real_pricing_rent_dict,real_pricing_transport_dict):
    text_message = f"""
        📌 Планирование путешествия: *{trip['name']}*

🗓 Даты: {trip['start_date']} — {trip['end_date']}
📍 Описание: {trip['description']}

💰 Бюджет: {trip['budget']['total']} {trip['budget']['currency']}""" + "\n".join([f"- {expense['category']}: {expense['amount']} {trip['budget']['currency']}" for expense in
trip['budget']['expenses']])

    text_liv = "Проживание:"

    for destination in trip['destinations']:
        text_message += f"""
🌍 Маршрут:
{destination['city']}, {destination['country']} ({destination['arrival_date']} — {destination['departure_date']})
- [{text_liv}]({build_travel_links(data_prev["city_from"], destination['city'], destination['arrival_date'], destination['departure_date'])["booking"]}) {" ".join(real_pricing_rent_dict[destination['city']])}/ночь
- Активности:""" + "\n" + "\n".join([
       f"- {act['name']} ({act['date']} {act['time']}), стоимость: {act['cost']} {trip['budget']['currency']}" for act in destination['activities']])

        text_message += f"\n\n✈️ Транспорт:"
        for transport in trip['transport']:
            text_message += f"""
- [{transport['type']}]({build_travel_links(transport['departure']['city'], transport['arrival']['city'], transport['departure']['date'], transport['departure']['date'])["google_flights"]}): {transport['departure']['city']} → {transport['arrival']['city']} ({transport['departure']['date']} {transport['departure']['time']})
- Примерная стоимость: {" ".join(real_pricing_transport_dict[f'{transport['departure']['city']}-{transport['arrival']['city']}'])}"""

        text_message += "\n\n✅ Чеклист:"
        for item in trip['checklist']:
            status = "✓" if item['completed'] else " "
            text_message += f"\n- [{status}] {item['item']}"

        text_message += f"\n\n📝 Заметки:\n{trip['notes']}"

        return text_message