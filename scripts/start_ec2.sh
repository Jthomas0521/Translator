# Using the echo keyword makes this prompt exit without users having to type Q
echo $(source .env && aws ec2 start-instances --instance-ids $AWS_INSTANCE_ID)
echo ""
echo "Wait about 30 seconds while your workstation boots."
echo "You can check the status of the workstation by running the command"
echo "\"scripts/ec2_status.sh\""

