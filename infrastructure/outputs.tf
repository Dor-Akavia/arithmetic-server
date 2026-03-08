output "jenkins_public_ip" {
  description = "Public IP address of the Jenkins EC2 instance"
  value       = aws_instance.jenkins.public_ip
}

output "jenkins_url" {
  description = "URL to access Jenkins web UI"
  value       = "http://${aws_instance.jenkins.public_ip}:8080"
}

output "ssh_command" {
  description = "SSH command to log in to the Jenkins server"
  value       = "ssh -i <your-key.pem> ubuntu@${aws_instance.jenkins.public_ip}"
}
