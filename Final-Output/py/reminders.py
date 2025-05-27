# Tagle, Marc Neil V.

from datetime import datetime
from plyer import notification


def days_until_birthday(birth_date_str):
    today = datetime.today().date()
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
    this_year_birthday = birth_date.replace(year=today.year)

    if this_year_birthday < today:
        next_birthday = this_year_birthday.replace(year=today.year + 1)
    else:
        next_birthday = this_year_birthday

    return (next_birthday - today).days


def group_by_upcoming(birthdays):
    grouped = {
        "Today": [],
        "This Week": [],
        "Next Week": [],
        "Upcoming": []
    }

    for person in birthdays:
        days_left = days_until_birthday(person['birth_date'])

        if days_left == 0:
            grouped["Today"].append((person, days_left))
        elif 1 <= days_left <= 7:
            grouped["This Week"].append((person, days_left))
        elif 8 <= days_left <= 14:
            grouped["Next Week"].append((person, days_left))
        else:
            grouped["Upcoming"].append((person, days_left))

    return grouped


def notify_upcoming_birthdays(grouped):
    for group in ["Today", "This Week", "Next Week"]:
        people_msgs = []
        for person, days_left in grouped.get(group, []):
            if not person.get("enabled", True):
                continue

            name = f"{person['first_name']} {person['last_name']}"

            if group == "Today":
                people_msgs.append(f"{name}")
            else:
                people_msgs.append(f"{name} ({days_left} {'day' if days_left == 1 else 'days'})")

        if people_msgs:
            print("NOTIFICATION:", people_msgs)
            
            message = "\n".join(people_msgs)
            notification.notify(
                title=f"Birthdays {group}",
                message=message,
                timeout=10,
                app_name="Birthday Tracker"
            )