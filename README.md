# Gym Membership Management System

## Overview

The Gym Membership Management System is an intuitive application designed to manage gym memberships and subscriptions effectively. The system supports three main activities:

- __Bodybuilding__
- __CrossFit__
- __Mixed Martial Arts (MMA)__

The system includes secure QR code functionality enhanced with encryption for smooth member check-ins and offers multiple subscription types to suit different needs.

## Features

- __Member Management__: Add and update member information.

- __Subscription Tracking__: Manage various subscription types and monitor their status.

- __Activity Selection__: Members can choose from Bodybuilding, CrossFit, or MMA.

- __Encrypted QR Code Integration__: Generate secure, encrypted QR codes for each member to ensure safe access.

## Subscription Methods

1. __Monthly Subscription__:

- Valid for one month from the entry date to the end date.
- If more than 30 days have passed since the subscription started, the subscription is considered expired.

2. __20-Session Subscription__:

- Members are allowed 20 gym entries.
- Each entry reduces the remaining session count by 1.
- Once the session count reaches 0, a renewal is required.

3. __30-Session Subscription__:

- Members are allowed 30 gym entries.
- Each entry reduces the remaining session count by 1.
- Once the session count reaches 0, a renewal is required.

## QR Code Functionality

- __Encrypted QR Code Generation__: QR codes are encrypted to protect member data.
- __Efficient Check-In__: Members scan their encrypted QR codes for secure and swift access.
- __Enhanced Security__: Encryption ensures data security, reducing unauthorized access risks.

## Technologies Used

- __Frontend and Backend__: Python with Kivy for a cross-platform user interface.
- __Database__: SQLite3 for storing member and subscription data.
- __Encryption__: Applied to QR codes to enhance security and data protection.

## Installation
1. __Clone the Repository__:

```bash
git clone https://github.com/Adib-96/gym_system.git
cd gym-system
```
2. __Install Dependencies__: Ensure you have Python and Kivy installed. If not, install them using:
```bash
pip install -r requirements.txt
```
3. __Run the Application__
```
python3 PowerPlanner.py
```
## Usage

1. __Register Members__: Add new member details, including their chosen subscription type and activities.
2. __Update Member Information__: Edit existing member profiles and subscription details as needed.
3. __Track Subscriptions__: Monitor subscription statuses, whether based on time (monthly) or session count (20 or 30 sessions).
4. __Secure Check-In__: Members scan their encrypted QR code at the gym entrance. The system automatically updates the session count or checks the subscription validity.
5. __Subscription Renewal__: When a subscription expires (monthly) or session count reaches 0, prompt the member for renewal.

## Future Enhancements
1. __Website for Members__: Develop a website where members can track their entry history and monitor their progress.
2. __Progress Badges__: Introduce a badge system similar to Discord. Members will earn badges for milestones, such as attending regularly for 3 or 4 months, to encourage continued participation.
3. __Incentive Gifts__: Offer gifts to members who attend the gym successfully for 6 consecutive months as a reward for their commitment.
4. __Mobile App Expansion__: Develop a mobile app for members to manage profiles and subscriptions on the go.
5. __Notification System__: Implement reminders for subscription renewals via email or SMS.
Detailed Analytics: Offer insights into gym usage, member activity, and trends.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for review.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Author
This Gym Membership Management System was created and developed by Adib ben Haddada. I'm dedicated to combining technology with fitness to create tools that make gym management more efficient and engaging for everyone. Feel free to connect with me for any feedback or collaboration opportunities.
