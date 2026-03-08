terraform {
  backend "s3" {
    bucket         = "jenkins-calculator-tf-state"
    key            = "dev/terraform.tfstate"
    region         = "eu-north-1"
    dynamodb_table = "jenkins-calculator-tf-locks"
    encrypt        = true
  }
}
