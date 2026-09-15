from pathlib import Path
from html import escape
from urllib.parse import unquote
import re, shutil
ROOT=Path(__file__).resolve().parent
FORM='https://form.respondi.app/n3RiRFmz'
original=(ROOT/'template.html').read_text(encoding='utf-8')
lines=[x.strip() for x in (ROOT/'content.txt').read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def t(prefix): return escape(next(x for x in lines if x.startswith(prefix)))
def paragraphs(*prefixes): return '<br><br>'.join(t(x) for x in prefixes)
html=original
mapping={
'Home':'Início','Features':'Pilares','About':'Experiência','Pricing':'Seleção','Blog':'Condução','Contact':'Aplicação','Cart':'Vagas',
'Book a Demo':'Aplicar para o PAC','Whats New':'Imersão gratuita','Ease Update v0.1':'2 dias · Londrina/PR',
'Intelligent Solutions Powered by AI.':t('Agenda cheia não'),
'Gain clarity and harness the power of your data with RedSun. Our intuitive dashboard provides real-time analytics.':paragraphs('Descubra o que','Uma imersão presencial de 2'),
'Read More':'Conheça os pilares','Join 4,000+ companies already growing':'PAC — Programa de Aceleração de Clínicas · Até 30 médicos',
'Balance':'Precificação','Users':'Posicionamento','Create':'Vendas','AI Sessions':'Gestão',
'Powerful Features':t('As alavancas que'),
"Explore the frontier of coding evolution with RedSun Unleashed. Our latest features redefine the boundaries of what's possible in coding tools.":paragraphs('Dois dias para olhar','Uma imersão presencial criada'),
'Top Management, to help you see the bigger picture':'Estrutura para escala',
'Helping you with fast-reading charts on the go':t('Profundidade, discussão'),
'See Doc':'Aplicar para o PAC','Customizable layouts for efficient coding.':'Precificação e posicionamento','Font preferences to match your style.':'Processo comercial e vendas','Create multiple profiles for versatility.':'Gestão, indicadores e equipe',
'Pricing Plans for Success':t('Uma seleção em três'),
'Discover the perfect plan for your coding journey with RedSun. Our pricing options are designed to provide you with the flexibility':paragraphs('Esta edição será limitada','O preenchimento da aplicação'),
'$49 USD':'01','Basic plan':'Aplique','$79 USD':'02','Business plan':'Análise','$90 USD':'03','Enterprise plan':'Seleção','Get started':'Aplicar para o PAC',
'Access to all basic features':'Até 30 médicos','Basic reporting and analytics':'2 dias presenciais','Up to 10 individual users':'Londrina/PR','20GB individual data each user':'Gratuita para selecionados','Basic chat and email support':'Mediante aplicação','20GB Easter Egg Text':'Sem compromisso de compra',
'Insights &amp; Inspiration':'Com Dr. Daniel Botelho.',
"Dive into the heart of innovation with our 'Coding Chronicles' blog section. Explore a rich tapestry of articles, tutorials, and insights that unravel.":t('A imersão será conduzida'),
'Digital Age':'Quem conduz','Misconceptions':'Legacy Doctors','Web Design':'Resultados e provas',
'Transform Your Work with Redsun':t('Se sua agenda já está'),
'Embark on a transformative journey of coding excellence with Redsun':paragraphs('Pode ser estruturar','O PAC reunirá'),
'Aliquam et tellus urna. Phasellus egetadipiscing elit. Mauris id nunc odio. Aliquam et tellus urna.':'PAC — Programa de Aceleração de Clínicas. Uma iniciativa do ecossistema Legacy Doctors.',
'Main Pages':'O programa','Blog Post':'Informações práticas','Pricing Single':'Como funciona','Checkout':'Aplicar para o PAC',
'Social media':'A experiência','Instagram':'Londrina/PR','Facebook':'2 dias presenciais','Linkedin':'Até 30 médicos','Twitter':'Participação gratuita',
'Webflow stuff':'Saiba mais','Style Guide':'Para quem é','Licensing':'Curadoria','Instructions':'FAQ','Change Log':'Aplicação',
'Created by':'Ecossistema','OVERSIGHT':'Legacy Doctors','Powered by':'Condução','WEBFLOW':'Dr. Daniel Botelho',
'Thank you!':'Obrigado!','Your submission has been received!':'Continue sua aplicação no formulário do PAC.','Oops!':'Atenção!','Something went wrong! Try again later':'Acesse o formulário para enviar sua aplicação.'}
special={
'Lorem ipsum dolor sit amet consectetur. Molestie lorem arcu':iter([t('Saia da lógica'),t('Construa uma percepção'),t('Estruture um processo'),t('Organize a operação')]),
'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas massa massa id arcu blandit dignissim contum volutpat dolor fermentum, justo tempor.':iter([t('Identifique gargalos'),t('Os participantes aprofundarão')]),
'Vulputate enim ante egestas commodo in.':iter(['Gestão · Posicionamento · Precificação · Marketing · Vendas · Processos · Estrutura comercial · Crescimento','Processos, crescimento e escala. Imersão presencial de 2 dias em Londrina/PR.']),
'Lorem ipsum dolor sit amet consectetur metus massa et amet cursus sit semper justo nascetur sem sapien ultrices nec aenean diam quisque.':iter([t('Preencha o formulário')]*2+[t('A equipe analisará')]*2+[t('Os médicos mais alinhados')]*2),
'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas massa massa id.':iter([t('Trajetória profissional'),t('O PAC faz parte'),'+200% '+t('de aumento no ticket')+'<br><br>'+t('Os resultados apresentados')])}
# Replace text nodes only; all original markup, image variants and animation scripts remain.
def replace_text(m):
    raw=m.group(1); key=raw.strip()
    if key in special: return '>'+next(special[key])+'<'
    return '>'+mapping.get(key,raw)+'<'
html=re.sub(r'>([^<>]+)<',replace_text,html)
html=html.replace('lang="en"','lang="pt-BR"').replace('RedSun - Webflow Ecommerce website template','PAC — Programa de Aceleração de Clínicas | Legacy Doctors')
html=html.replace('<body>','<body id="inicio">').replace('id="readmore"','id="pilares"')
for cls,anchor in [('new-features-holder','experiencia'),('pricing-wrapper','selecao'),('blog-grid-3x-holder','conducao'),('cta-wrapper','aplicacao')]:
    html=html.replace('class="'+cls+'"','id="'+anchor+'" class="'+cls+'"',1)
hrefs={'/':'#inicio','/features':'#pilares','/about':'#experiencia','/pricing':'#selecao','/blog':'#conducao','/contact':FORM,'#readmore':'#pilares','https://Google.com':FORM,'/checkout':FORM,'https://instagram.com':'#informacoes','https://fb.com':'#experiencia','https://linkedin.com':'#selecao','https://twitter.com':'#curadoria','/template/style-guide':'#para-quem','/template/licensing':'#curadoria','/template/instructions':'#faq','/template/change-log':FORM,'http://madebyoversight.com/':'#conducao','https://webflow.com/':'#conducao'}
def replace_anchor(m):
    tag=m.group(0); match=re.search(r'href="([^"]*)"',tag)
    if not match:return tag
    old=match.group(1); new=hrefs.get(old,old)
    if '/product/' in old:new=FORM
    if '/post/' in old:new='#conducao'
    if 'button-glow' in tag or 'button-simple' in tag and old!='#readmore':new=FORM
    if 'ease-badge' in tag:new='#informacoes'
    if 'commerce-cart-open-link' in tag:
        new='#selecao'
        tag=re.sub(r' data-node-type="commerce-cart-open-link"| aria-haspopup="dialog"| role="button"','',tag)
        tag=tag.replace('aria-label="Open cart"','aria-label="Até 30 vagas"')
    tag=tag.replace('href="'+old+'"','href="'+new+'"')
    if new==FORM and 'target=' not in tag:tag=tag[:-1]+' target="_blank" rel="noopener noreferrer">'
    return tag
html=re.sub(r'<a\b[^>]*>',replace_anchor,html)
html=re.sub(r'<div[^>]*class="w-commerce-commercecartopenlinkcount cart-number"[^>]*>0</div>','<div class="cart-number">30</div>',html)
html=re.sub(r'(<div[^>]*class="[^"]*cart-quantity[^\"]*"[^>]*>)0(<)',r'\g<1>30\2',html)
# The original CTA panel and its animated dashboard remain; applications use Respondi.
html=re.sub(r'<form id="Early-Access-Emails".*?</form>',f'<div class="form-holder"><div class="form"><a class="button-glow w-inline-block" href="{FORM}" target="_blank" rel="noopener noreferrer">Aplicar para o PAC</a></div></div>',html,flags=re.S)
def p(prefix):return '<p>'+t(prefix)+'</p>'
def section(id,kicker,title,content):return f'<section id="{id}" class="section pac-extra"><div class="container"><div class="section-paddings"><div class="section-center-text"><p class="pac-kicker">{kicker}</p><h2 class="title medium">{t(title)}</h2></div>{content}</div></div></section>'
def ul(prefixes):return '<ul>'+''.join('<li>'+t(x)+'</li>' for x in prefixes)+'</ul>'
extra=section('para-quem','Para quem é','Excelência técnica',f'<div class="pac-columns"><div>{p("Se sua agenda está cheia, mas")}{p("Muitos médicos tentam")}{p("Mas crescimento de volume")}</div><div>{ul(["Médicos donos de clínica","Profissionais em fase","Médicos com demanda","Clínicas sem processo","Profissionais que querem","Médicos que desejam"])}{p("Uma experiência para médicos")}</div></div>')
extra+=section('margem','Volume versus margem','Atender mais não',f'<div class="pac-columns"><div class="home-grid-box pac-box"><h3>O ciclo que aumenta complexidade</h3><p>01 Mais pacientes<br>02 Mais trabalho<br>03 Mais equipe<br>04 Mais custos<br>05 Mais complexidade</p></div><div class="home-grid-box pac-box"><h3>Uma lógica mais eficiente</h3>{p("Posicionamento +")}{p("Crescimento com maior")}{p("Uma direção estratégica")}</div></div>')
extra+=section('curadoria','Curadoria','O PAC não será',f'<div class="pac-columns"><div>{p("Esta edição será limitada")}{ul(["Não é venda","Não é inscrição","A aplicação não garante","Existe um processo"])}</div><div><h3>Por que a participação é gratuita</h3>{p("Nesta edição piloto")}{p("Transporte, hospedagem")}</div></div>')
extra+=section('informacoes','Informações práticas','Uma experiência presencial e concentrada.', '<dl class="pac-info">'+''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k,v in [('Programa','PAC — Aceleração de Clínicas'),('Formato','Presencial'),('Duração','2 dias'),('Local','Londrina/PR'),('Vagas','Até 30 médicos'),('Condução','Dr. Daniel Botelho'),('Ecossistema','Legacy Doctors'),('Participação','Gratuita para selecionados'),('Entrada','Mediante aplicação'),('Data','A definir')])+'</dl>')
faqs=[('O PAC é gratuito?','Nesta edição piloto, não haverá cobrança de ingresso. Os médicos selecionados poderão participar sem custo de inscrição. Transporte, hospedagem, alimentação e demais despesas não estão confirmados como inclusos.'),('Qualquer médico pode participar?','O PAC é voltado a médicos donos de clínicas e cirurgiões plásticos. Cada aplicação será analisada, e serão selecionados os profissionais mais alinhados à proposta da experiência.'),('Preencher o formulário garante uma vaga?','Não. O preenchimento da aplicação é a primeira etapa do processo de seleção e não garante participação.'),('Quantos médicos serão selecionados?','Esta edição será limitada a até 30 médicos.'),('Onde acontecerá?','Em Londrina, no Paraná. A data está a definir.'),('Quanto tempo dura?','A imersão tem duração de 2 dias presenciais.'),('Quem conduz o programa?','Dr. Daniel Botelho, em uma iniciativa do ecossistema Legacy Doctors.'),('Preciso informar meu faturamento?','Não há solicitação de faturamento nesta etapa da aplicação.')]
extra+=section('faq','FAQ','Perguntas frequentes.', '<div class="pac-faq">'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)+'</div>')
extra+=f'<section class="section pac-extra"><div class="container"><div class="pac-columns"><div><h2>Aplicar para o PAC.</h2>{p("Preencha suas informações")}{ul(["Sem cobrança de ingresso","Sem compromisso de compra","Sem solicitação de faturamento"])}</div><div><p>Nome completo · WhatsApp · Cidade / UF · Instagram · Especialidade médica</p><a class="button-glow w-inline-block" href="{FORM}" target="_blank" rel="noopener noreferrer">Preencher aplicação</a>{p("Após o envio")}</div></div><div class="pac-material"><h3>Resultados e provas</h3><p>Depoimentos em vídeo · Histórias de médicos · Cases da metodologia · Resultados específicos</p><p>Material em atualização</p></div></div></section>'
html=html.replace('<div data-w-id="8ed71055-6ae7-5324-a6d4-54fc76e0e2d9"',extra+'<div data-w-id="8ed71055-6ae7-5324-a6d4-54fc76e0e2d9"',1)
html=html.replace('</head>','<link rel="stylesheet" href="css/pac-restored.css"></head>')
images=re.findall(r'<img\b[^>]*>',original)
assert images==re.findall(r'<img\b[^>]*>',html),'Original image markup changed'
hooks=re.findall(r'data-w-id="([^"]+)"',original)
assert hooks==re.findall(r'data-w-id="([^"]+)"',html),'Animation IDs changed'
assert re.findall(r'<script\b.*?</script>',original,re.S)==re.findall(r'<script\b.*?</script>',html,re.S),'Scripts changed'
# Brand substitutions are restricted to logos; the restored illustration and animation markup stays intact.
before_brand=html
def brand_logo(match):
    tag=match.group(0)
    if 'class="brand-image"' in tag or 'class="footer-brand-image"' in tag:
        tag=re.sub(r'src="[^"]+"','src="images/legacy/logo-gold-white.png"',tag)
        tag=tag.replace('alt=""','alt="Legacy Doctors"')
    elif 'class="company-logo"' in tag:
        tag=re.sub(r'src="[^"]+"','src="images/legacy/logo-white.png"',tag)
        tag=tag.replace('alt=""','alt="Legacy Doctors"')
    return tag
html=re.sub(r'<img\b[^>]*>',brand_logo,html)
html=html.replace('images/673c86594c8e945d0a8d39fd_Fav.png','images/legacy/brand-icon.png').replace('images/673c865c3de8eb55a5db0099_Web.png','images/legacy/brand-icon.png')
html=html.replace('</head>','<link rel="stylesheet" href="css/legacy-brand.css"></head>')
assert len(images)==len(re.findall(r'<img\b[^>]*>',html))
assert hooks==re.findall(r'data-w-id="([^"]+)"',html)
nonlogo=lambda s:[x for x in re.findall(r'<img\b[^>]*>',s) if not any(c in x for c in ['class="brand-image"','class="footer-brand-image"','class="company-logo"'])]
assert nonlogo(before_brand)==nonlogo(html), 'Non-brand imagery changed'
(ROOT/'index.html').write_text(html,encoding='utf-8')
for ref in re.findall(r'(?:src|href)="((?:images|css|js)/[^"?#]+)"',html):assert (ROOT/unquote(ref)).is_file(),ref
for group in re.findall(r'srcset="([^"]+)"',html):
    for candidate in group.split(','):
        ref=candidate.strip().rsplit(' ',1)[0];assert (ROOT/unquote(ref)).is_file(),ref
ids=set(re.findall(r'id="([^"]+)"',html))
assert all(a in ids for a in re.findall(r'href="#([^"]+)"',html))
assert 'Lorem ipsum' not in html
dist=ROOT/'dist';dist.mkdir(exist_ok=True)
shutil.copy2(ROOT/'index.html',dist/'index.html')
for folder in ('css','images','js','fonts'):shutil.copytree(ROOT/folder,dist/folder,dirs_exist_ok=True)
print('Restored',len(images),'original images and',len(hooks),'animation hooks. Scripts, images, variants and links verified.')
