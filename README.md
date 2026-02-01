# T-Pot AWS Honeypot

This project deploys a **T-Pot honeypot on AWS** to capture real-world attack activity and analyze basic security patterns.

## Purpose
- Learn how honeypots work in a cloud environment
- Observe common attack behavior
- Analyze logs from honeypots and IDS tools
- Practice defensive security and incident analysis skills

## Setup Overview
1. Create an EC2 instance in AWS
2. Install and configure T-Pot
3. Allow controlled inbound traffic using Security Groups
4. Monitor attacks through the T-Pot dashboard
5. Export logs for basic analysis

Detailed steps are documented in the `docs/` folder.

## What is collected
- Network and honeypot logs
- IDS alerts
- Basic connection and authentication attempts

## Analysis
Python scripts in the `analysis/` folder summarize:
- Most targeted ports
- Frequently attacked services
- Top source IP addresses

## Notes
- This project is for **defensive security learning only**
- The honeypot is isolated and does not contain real data


## Tools Used
- AWS EC2
- T-Pot
- Python
- Linux



