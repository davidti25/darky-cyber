# ==============================================================================
# 🤖 Cisco NetAcad Auto Crawler & Content Ingestor
# ==============================================================================
# Autor: Darky Cyber & Antigravity Copilot
# Descrição: Navega automaticamente pela turma da Cisco NetAcad, abre todos os
#            módulos (do 8 ao 39), intercepta os dados do Adapt Learning e salva
#            100% dos textos e quizzes organizados por pasta.
# ==============================================================================

import os
import re
import json
import asyncio
import sys
from pathlib import Path
from urllib.parse import urlparse
from playwright.async_api import async_playwright

# Configura encoding UTF-8 no Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Path do scraper
SCRAPER_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRAPER_DIR))

from config_loader import load_config
from cisco_adapt_parser import parse_adapt_components

BASE_OUTPUT_DIR = SCRAPER_DIR.parent / "courses" / "cisco_academy" / "conceitos_basicos_de_redes"
BASE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_COURSE_URL = "https://www.netacad.com/pt/launch?id=26f8e8e3-dff7-47e4-956d-e7aa203b5447&tab=curriculum"

class CiscoAutoCrawler:
    def __init__(self, headless=False):
        self.config = load_config()
        self.headless = headless
        self.user_data_dir = SCRAPER_DIR / ".browser_data" / "cisco"
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self.captured_modules = set()
        self.current_crawling_module = None

    def extract_module_id(self, url: str, data=None) -> str:
        url_lower = url.lower()
        
        # 1. Tenta extrair da URL (ex: /m8/, /m08/, /content/m8/)
        match = re.search(r'/(m\d{1,2})/', url_lower)
        if match:
            return match.group(1)

        # 2. Tenta extrair de course.json ou título se tiver
        if isinstance(data, dict):
            title = data.get('title') or data.get('displayTitle') or ''
            mod_match = re.search(r'm[oó]dulo\s*(\d+)', title, re.IGNORECASE)
            if mod_match:
                return f"m{mod_match.group(1)}"

        # 3. Se for lista de componentes, checa se tem título com módulo
        if isinstance(data, list) and len(data) > 0:
            for item in data[:5]:
                if isinstance(item, dict):
                    t = item.get('title') or ''
                    mod_match = re.search(r'm[oó]dulo\s*(\d+)', t, re.IGNORECASE)
                    if mod_match:
                        return f"m{mod_match.group(1)}"

        # 4. Fallback para o módulo ativo no loop
        if self.current_crawling_module:
            return self.current_crawling_module

        return "desconhecido"

    async def handle_network_response(self, response):
        url = response.url
        url_lower = url.lower()

        # Intercepta qualquer resposta JSON relevante do curso
        is_json_candidate = (
            url_lower.endswith(".json") or 
            "components" in url_lower or 
            "articles" in url_lower or 
            "course" in url_lower or
            "contentobjects" in url_lower or
            "blocks" in url_lower
        )

        if not is_json_candidate:
            return

        try:
            if response.status == 200:
                data = await response.json()
                
                # Identifica se é conteúdo do Adapt Learning
                is_adapt = False
                filename = "data.json"

                if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and "_component" in data[0]:
                    is_adapt = True
                    filename = "components.json"
                elif isinstance(data, dict) and ("_latestTrackingId" in data or "_buttons" in data):
                    is_adapt = True
                    filename = "course.json"
                elif "articles" in url_lower:
                    is_adapt = True
                    filename = "articles.json"
                elif "blocks" in url_lower:
                    is_adapt = True
                    filename = "blocks.json"
                elif "contentobjects" in url_lower:
                    is_adapt = True
                    filename = "contentObjects.json"

                if is_adapt:
                    mod_id = self.extract_module_id(url, data)
                    if mod_id != "desconhecido":
                        mod_dir = BASE_OUTPUT_DIR / mod_id / "raw"
                        mod_dir.mkdir(parents=True, exist_ok=True)

                        file_path = mod_dir / filename
                        with open(file_path, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)

                        print(f"📦 [CAPTURADO] Módulo {mod_id.upper()}: {filename}")
                        self.captured_modules.add(mod_id)

                        # Se capturou components.json, executa o parser imediatamente
                        if filename == "components.json":
                            parsed = parse_adapt_components(data)
                            parsed_path = BASE_OUTPUT_DIR / mod_id / "parsed_content.json"
                            with open(parsed_path, "w", encoding="utf-8") as f:
                                json.dump(parsed, f, ensure_ascii=False, indent=2)
                            print(f"   ✅ [PARSER SUCESSO] {mod_id.upper()}: {len(parsed['sections'])} seções e {len(parsed['quizzes'])} questões salvas!")

        except Exception as err:
            # Ignora erros de parse de respostas transitórias
            pass

    async def run(self):
        print("\n" + "="*65)
        print("🤖 [Cisco Auto Crawler] Iniciando Varredura Automática...")
        print(f"📁 Diretório de destino: {BASE_OUTPUT_DIR}")
        print("="*65 + "\n")

        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(self.user_data_dir),
                headless=self.headless,
                viewport={"width": 1366, "height": 850},
                args=["--disable-blink-features=AutomationControlled"]
            )

            # Monitora todas as abas e janelas abertas
            context.on("page", lambda new_page: new_page.on("response", self.handle_network_response))

            page = context.pages[0] if context.pages else await context.new_page()
            page.on("response", self.handle_network_response)

            print(f"🌐 Navegando para o currículo da Turma do Prof. Felipe...")
            await page.goto(TARGET_COURSE_URL, wait_until="domcontentloaded")
            await asyncio.sleep(4)

            # Checa se caiu em tela de login
            current_url = page.url
            if "auth.netacad.com" in current_url or "login" in current_url:
                print("🔑 Tela de autenticação detectada. Preenchendo credenciais...")
                try:
                    email_input = await page.wait_for_selector('input[type="email"], input[name="username"], #username', timeout=5000)
                    if email_input:
                        await email_input.fill(self.config.get("CISCO_LOGIN", ""))
                        next_btn = await page.query_selector('button[type="submit"], #kc-login, #next')
                        if next_btn:
                            await next_btn.click()
                            await asyncio.sleep(2)

                    pass_input = await page.wait_for_selector('input[type="password"], #password', timeout=5000)
                    if pass_input:
                        await pass_input.fill(self.config.get("CISCO_PASS", ""))
                        login_btn = await page.query_selector('button[type="submit"], #kc-login')
                        if login_btn:
                            await login_btn.click()
                            print("🚀 Login submetido. Aguardando redirecionamento para o curso...")
                            await asyncio.sleep(6)
                except Exception as e:
                    print(f"ℹ️ Login manual ou verificação necessária: {e}")

            print("\n🔍 Analisando estrutura da página do curso...")
            await asyncio.sleep(4)

            # Loop inteligente de rastreamento de módulos 1 ao 7 e Checkpoints
            print("\n🎯 INICIANDO VARREDURA DOS MÓDULOS 1 AO 7 E CHECKPOINTS...")
            print("👉 O robô vai varrer os 7 primeiros módulos e os exames de verificação!\n")

            # Varredura dos Módulos 1 ao 7
            for mod_num in range(1, 8):
                self.current_crawling_module = f"m{mod_num}"
                print(f"⏳ Procurando Módulo {mod_num}...")
                try:
                    selectors = [
                        f"text=/M[oó]dulo {mod_num}\\b/i",
                        f"button:has-text('Módulo {mod_num}')",
                        f"a:has-text('Módulo {mod_num}')",
                        f"[role='button']:has-text('Módulo {mod_num}')"
                    ]
                    for sel in selectors:
                        el = await page.query_selector(sel)
                        if el and await el.is_visible():
                            print(f"👉 Clicando no Módulo {mod_num}...")
                            await el.scroll_into_view_if_needed()
                            await el.click()
                            await asyncio.sleep(3)
                            break

                    start_link = await page.query_selector("a:has-text('Iniciar'), button:has-text('Iniciar'), a:has-text('Introdução')")
                    if start_link and await start_link.is_visible():
                        await start_link.click()
                        await asyncio.sleep(3)
                except Exception:
                    pass
                await asyncio.sleep(1)

            # Varredura dos Exames de Ponto de Verificação
            print("\n🎯 INICIANDO VARREDURA DOS EXAMES DE CHECKPOINT...")
            checkpoints = [
                "Construir uma pequena rede",
                "acesso à rede",
                "o protocolo da Internet"
            ]

            for cp_name in checkpoints:
                self.current_crawling_module = f"checkpoint_{cp_name.lower().replace(' ', '_')}"
                print(f"⏳ Procurando Exame: {cp_name}...")
                try:
                    cp_el = await page.query_selector(f"text=/{cp_name}/i")
                    if cp_el and await cp_el.is_visible():
                        print(f"👉 Acessando Exame: {cp_name}...")
                        await cp_el.scroll_into_view_if_needed()
                        await cp_el.click()
                        await asyncio.sleep(4)
                except Exception:
                    pass

            print("\n🎉 Varredura concluída ou em andamento!")
            print("Você pode continuar navegando pela janela do navegador se faltar algum módulo específico.")
            print("Pressione Ctrl+C no terminal ou feche o navegador quando quiser finalizar.\n")

            # Mantém vivo para interceptar quaisquer cliques adicionais
            while True:
                await asyncio.sleep(2)
                if not context.pages:
                    break

if __name__ == "__main__":
    crawler = CiscoAutoCrawler(headless=False)
    try:
        asyncio.run(crawler.run())
    except KeyboardInterrupt:
        print("\n[INFO] Varredura finalizada pelo usuário.")

