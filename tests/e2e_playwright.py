from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:5000'

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Registro de paciente
        page.goto(f"{BASE}/register")
        page.fill('input[name="nombre"]', 'E2E Paciente')
        page.fill('input[name="correo"]', 'e2e_paciente@example.com')
        page.fill('input[name="password"]', 'e2ePwd123')
        page.fill('input[name="documento"]', '12345678')
        page.fill('input[name="telefono"]', '3001112222')
        page.click('button[type="submit"]')

        # Login paciente
        page.goto(BASE)
        page.fill('input[name="email"]', 'e2e_paciente@example.com')
        page.fill('input[name="password"]', 'e2ePwd123')
        page.click('button[type="submit"]')

        # Aquí se podrían navegar las páginas de reserva y crear cita
        print('Registro y login de paciente ejecutados (verificar manualmente las páginas).')

        browser.close()

if __name__ == '__main__':
    run()
