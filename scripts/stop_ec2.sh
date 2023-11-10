# Using the echo keyword makes this prompt exit without users having to type Q
echo $(source .env && aws ec2 stop-instances --instance-ids $AWS_INSTANCE_ID)