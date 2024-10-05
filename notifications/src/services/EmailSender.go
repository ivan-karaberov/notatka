package services

import (
	"log"

	"gopkg.in/gomail.v2"
)

// Настройки для электронной почты
type EmailConfig struct {
	SMTPHost string
	SMTPPort int
	Username string
	Password string
}

// Отправка сообщения на почту
func SendEmail(config EmailConfig, to string, subject string, body string) error {
	m := gomail.NewMessage()
	m.SetHeader("From", config.Username)
	m.SetHeader("To", to)
	m.SetHeader("Subject", subject)
	m.SetBody("text/plain", body)

	d := gomail.NewDialer(config.SMTPHost, config.SMTPPort, config.Username, config.Password)

	if err := d.DialAndSend(m); err != nil {
		log.Fatal(err)
	}

	return nil
}
