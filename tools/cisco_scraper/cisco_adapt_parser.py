import re
import html
import json
import sys
from pathlib import Path

# Configura encoding UTF-8 no Windows para evitar UnicodeEncodeError
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

def clean_html(raw_html: str) -> str:
    """Remove tags HTML mantendo a estrutura limpa de texto."""
    if not raw_html:
        return ""
    # Substitui quebras de linha e paragrafos por newlines
    text = re.sub(r'</?(p|div|h[1-6]|li|br)[^>]*>', '\n', raw_html)
    # Remove qualquer outra tag
    text = re.sub(r'<[^>]+>', '', text)
    # Decodifica entidades HTML (&nbsp;, &atilde;, etc)
    text = html.unescape(text)
    # Remove multiplos espacos e quebras excessivas
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)

def parse_adapt_components(components_list: list) -> dict:
    """
    Analisa a lista de componentes do Adapt Learning da Cisco e separa
    entre secoes de conteudo textual/visual e questoes de fixacao/quizzes.
    """
    sections = []
    quizzes = []
    images = []

    for comp in components_list:
        comp_type = comp.get('_component')
        title = comp.get('title') or ""
        body = comp.get('body') or ""
        instruction = comp.get('instruction') or ""

        # Remove variaveis do Adapt como {{_moduleNumber}}
        title_clean = title.replace('{{_moduleNumber}}', '').strip()

        # 1. Questoes de multipla escolha (MCQ / GMCQ)
        if comp_type in ['mcq', 'gmcq']:
            items = comp.get('_items', [])
            options = []
            correct_index = -1

            for idx, opt in enumerate(items):
                opt_text = clean_html(opt.get('text', ''))
                options.append(opt_text)
                if opt.get('_shouldBeSelected', False):
                    correct_index = idx

            # Feedback oficial da questao
            feedback = comp.get('_feedback', {})
            correct_feedback = clean_html(feedback.get('correct', ''))
            
            quizzes.append({
                "question": clean_html(body) or title_clean,
                "options": options,
                "correctIndex": correct_index,
                "explanation": correct_feedback,
                "raw_id": comp.get('_id')
            })

        # 2. Imagens e Graficos
        elif comp_type in ['graphic', 'dynamic-graphic']:
            graphic_data = comp.get('_graphic', {})
            src = graphic_data.get('src') or comp.get('src')
            alt = graphic_data.get('alt') or comp.get('alt') or title_clean
            if src:
                images.append({"src": src, "alt": alt, "title": title_clean})
            if body:
                sections.append({
                    "type": "graphic_text",
                    "title": title_clean,
                    "content": clean_html(body),
                    "image": src
                })

        # 3. Textos e Artigos
        elif comp_type == 'text':
            cleaned_body = clean_html(body)
            if cleaned_body:
                sections.append({
                    "type": "text",
                    "title": title_clean,
                    "content": cleaned_body
                })

        # 4. Acordions e Abas interativas
        elif comp_type == 'accordion':
            items = comp.get('_items', [])
            acc_content = []
            for it in items:
                it_title = clean_html(it.get('title', ''))
                it_body = clean_html(it.get('body', ''))
                if it_title or it_body:
                    acc_content.append(f"**{it_title}:** {it_body}")
            sections.append({
                "type": "accordion",
                "title": title_clean,
                "content": '\n\n'.join(acc_content)
            })

    return {
        "sections": sections,
        "quizzes": quizzes,
        "images": images
    }

def parse_module_directory(module_path: Path, save_output: bool = True) -> dict:
    """
    Processa um diretorio de modulo (ex: courses/.../m4 ou .../m4/raw),
    localizando components.json e gerando parsed_content.json.
    """
    target_dir = module_path
    if (module_path / "raw").exists():
        raw_components = module_path / "raw" / "components.json"
        output_dir = module_path
    elif module_path.name == "raw":
        raw_components = module_path / "components.json"
        output_dir = module_path.parent
    else:
        raw_components = module_path / "components.json"
        output_dir = module_path

    if not raw_components.exists():
        raise FileNotFoundError(f"Arquivo components.json nao encontrado em {raw_components}")

    with open(raw_components, "r", encoding="utf-8") as f:
        components_data = json.load(f)

    parsed = parse_adapt_components(components_data)

    if save_output:
        output_file = output_dir / "parsed_content.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
        print(f"[PARSER] Modulo {output_dir.name} processado com sucesso:")
        print(f"  -> {len(parsed['sections'])} secoes de texto/acordeon")
        print(f"  -> {len(parsed['quizzes'])} questoes de fixacao")
        print(f"  -> {len(parsed['images'])} recursos visuais mapeados")
        print(f"  -> Salvo em: {output_file}")

    return parsed

def parse_all_available_modules(base_cisco_dir: Path = None):
    """Varre todos os modulos disponiveis no diretorio do curso e compila os parsed_content.json."""
    if base_cisco_dir is None:
        base_cisco_dir = Path(__file__).resolve().parent.parent / "courses" / "cisco_academy" / "conceitos_basicos_de_redes"

    if not base_cisco_dir.exists():
        print(f"[AVISO] Diretorio base nao encontrado: {base_cisco_dir}")
        return

    count = 0
    for mod_path in sorted(base_cisco_dir.glob("m*")):
        if mod_path.is_dir():
            comp_path = mod_path / "raw" / "components.json"
            if comp_path.exists():
                try:
                    parse_module_directory(mod_path, save_output=True)
                    count += 1
                except Exception as err:
                    print(f"[ERRO] Falha ao processar {mod_path.name}: {err}")
    print(f"\n[PARSER CONCLUIDO] Total de {count} modulos processados com sucesso.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = Path(sys.argv[1]).resolve()
        if target.is_file() and target.name == "components.json":
            parse_module_directory(target.parent, save_output=True)
        elif target.is_dir():
            parse_module_directory(target, save_output=True)
        else:
            print(f"[ERRO] Caminho invalido: {target}")
    else:
        parse_all_available_modules()
