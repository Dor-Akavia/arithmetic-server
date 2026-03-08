resource "aws_instance" "jenkins" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_pair_name
  vpc_security_group_ids = [aws_security_group.jenkins_sg.id]

  #Loads cloud-init data from seperate file
  user_data = templatefile("${path.module}/user_data.sh.tpl", {
  })

  tags = {
    Name = "jenkins-server"
  }
}



