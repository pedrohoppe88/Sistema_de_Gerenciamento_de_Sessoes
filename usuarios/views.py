from django.shortcuts import render, redirect
from .forms import UsuarioForm, UsuarioEditForm, LoginForm, SessaoForm
from .models import Retirada, Usuario
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Sessao, Item
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from .models import Sessao, Item
from django.db.models import Sum, Count

def cadastrar_usuario(request):
    """
    Renderiza o formulário de cadastro de novo usuário e processa o envio.

    Em caso de POST com dados válidos, salva o novo usuário e redireciona
    para a página de login. Em caso de GET, apenas exibe o formulário em branco.
    """
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/cadastrar.html', {
        'form': form,
        'graduacao_choices': Usuario.GRADUACAO_CHOICES
    })

def sucesso(request):
    """
    Página de sucesso exibida após o login bem-sucedido.

    Verifica se o usuário está logado através da sessão. Se não estiver,
    redireciona para a página de login. Caso contrário, exibe uma mensagem
    de boas-vindas com o nome e graduação do usuário.
    """
    if 'usuario_id' not in request.session:
        return redirect('login')

    usuario_id = request.session.get('usuario_id')
    usuario = Usuario.objects.get(id=usuario_id) if usuario_id else None
    nome = usuario.nome if usuario else None
    graduacao = usuario.graduacao if usuario else None
    return render(request, 'usuarios/sucesso.html', {'usuario_id': usuario_id, 'graduacao': graduacao, 'nome': nome})

def login_usuario(request):
    """
    Renderiza a página de login e processa a autenticação do usuário.

    Em caso de POST, valida o email e a senha. Se as credenciais estiverem
    corretas, armazena o ID do usuário na sessão e redireciona para a página
    'sucesso'. Caso contrário, exibe mensagens de erro no formulário.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            try:
                usuario = Usuario.objects.get(email=email)
                if check_password(senha, usuario.senha):
                    request.session['usuario_id'] = usuario.id
                    return redirect('sucesso')
                else:
                    form.add_error('senha', 'Senha incorreta.')
            except Usuario.DoesNotExist:
                form.add_error('email', 'Usuário não encontrado.')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_usuario(request):
    """
    Realiza o logout do usuário limpando todos os dados da sessão.

    Após limpar a sessão, redireciona o usuário para a página de login.
    """
    request.session.flush()
    return redirect('login')

def listar_usuarios(request):
    """
    Lista todos os usuários cadastrados.

    Esta view é protegida e exige que o usuário esteja logado.
    Busca todos os objetos Usuario e os envia para o template 'all_users.html'.
    Nota: Funcionalidade similar a `all_users`.
    """
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/all_users.html', {'usuarios': usuarios})

def all_users(request):
    """
    Exibe uma lista de todos os usuários com informações adicionais.

    Protegida por login, esta view busca todos os usuários e também injeta
    no contexto os dados do usuário logado (nome, graduação) e a contagem
    total de usuários.
    """
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuarios = Usuario.objects.all()
    usuario_id = request.session.get('usuario_id')
    user = Usuario.objects.get(id=usuario_id) if usuario_id else None
    nome = user.nome if user else None
    graduacao = user.graduacao if user else None
    quant_id = Usuario.objects.count()
    return render(request, 'usuarios/all_users.html', {
        'usuarios': usuarios,
        'id_usuario': usuario_id,
        'nome': nome,
        'graduacao': graduacao,
        'quantidade': quant_id
    })

def dashboard(request):
    """
    View para um painel de controle com estatísticas de usuários.

    Nota: A view parece estar incompleta, pois não há um `return render`.
    A lógica coleta estatísticas como total de usuários, usuários ativos
    e cadastros recentes, preparando um contexto para ser renderizado.
    """
    if 'usuario_id' not in request.session:
        return redirect('login')

    usuarios = Usuario.objects.all()

    total_usuarios = usuarios.count()
    usuarios_ativos = usuarios.filter(status='ativo').count()
    graduados_recentes = usuarios.order_by('-id')[:5].count()

    context = {
        'usuarios': usuarios,
        'total_usuarios': total_usuarios,
        'usuarios_ativos': usuarios_ativos,
        'graduados_recentes': graduados_recentes,
    }
    # Falta o `return render(request, 'template.html', context)`

def entrar_sessao(request, sessao_id):
    """
    Processa a entrada em uma sessão protegida por senha.

    Recebe um POST com a senha. Se a senha corresponder à da sessão,
    uma flag é definida na sessão do usuário para autorizar o acesso
    e ele é redirecionado para os detalhes da sessão. Caso contrário,
    uma mensagem de erro é exibida.
    """
    sessao = get_object_or_404(Sessao, id=sessao_id)
    
    if request.method  == "POST":
        senha = request.POST.get('senha')
        if sessao.senha == senha:
            request.session[f"sessao_{sessao.id}"] = True
            return redirect('detalhes_sessao', sessao_id=sessao.id)
        else:
            messages.error(request, 'Senha incorreta.')
            return render(request, "entrar_sessao.html", {"sessao": sessao})
    
def detalhes_sessao(request, sessao_id):
    """
    Exibe os detalhes e os itens de uma sessão específica.

    O acesso é permitido apenas se o usuário for o criador da sessão ou
    se tiver inserido a senha correta (verificado pela flag na sessão).
    """
    sessao = get_object_or_404(Sessao, id=sessao_id)

    if not request.user == sessao.criador and not request.session.get(f"sessao_{sessao.id}", False):
        messages.error(request, "Acesso negado!")
        return redirect("entrar_sessao", sessao_id=sessao.id)

    itens = sessao.itens.all()
    return render(request, "detalhes_sessao.html", {"sessao": sessao, "itens": itens})

def adicionar_item(request, sessao_id):
    """
    Adiciona um novo item a uma sessão específica.

    Disponível apenas para o criador da sessão ou para quem entrou com a senha.
    Processa um POST para criar um novo `Item` associado à sessão e
    redireciona para a lista de itens da mesma.
    """
    sessao = get_object_or_404(Sessao, id=sessao_id)

    if not request.user == sessao.criador and not request.session.get(f"sessao_{sessao.id}", False):
        messages.error(request, "Você não tem permissão!")
        return redirect("entrar_sessao", sessao_id=sessao.id)

    if request.method == "POST":
        nome = request.POST.get("nome")
        quantidade = int(request.POST.get("quantidade", 1))
        Item.objects.create(sessao=sessao, nome=nome, quantidade=quantidade)

        return redirect("listar_itens", sessao_id=sessao.id)

    return render(request, "adicionar_item.html", {"sessao": sessao})

def criar_sessao(request):
    """
    Renderiza e processa o formulário para criação de uma nova sessão.

    Acesso restrito a administradores. Em caso de POST com dados válidos,
    salva a nova sessão associada ao administrador logado.
    """
    if 'usuario_id' not in request.session:
        return redirect('login')

    usuario_id = request.session.get('usuario_id')
    criador = Usuario.objects.get(id=usuario_id) if usuario_id else None

    if not criador or not criador.is_admin:
        messages.error(request, "Acesso negado. Apenas administradores podem criar sessões.")
        return redirect('listar_sessoes')

    if request.method == "POST":
        form = SessaoForm(request.POST)
        if form.is_valid():
            form.saveSessao(criador=criador)
            messages.success(request, "Sessão criada com sucesso!")
            return redirect("listar_sessoes")
    else:
        form = SessaoForm()

    return render(request, "usuarios/criar_sessao.html", {'form': form})

def mostrar_sessao(request):
    """
    View de depuração simples para exibir o ID do usuário logado na sessão.
    """
    usuario_id = request.session.get('usuario_id')
    return HttpResponse(f"Usuário logado (usuario_id): {usuario_id}")

def listar_sessoes(request):
    """
    Exibe todas as sessões cadastradas para usuários logados.
    """
    if 'usuario_id' not in request.session:
        return redirect('login')
    sessoes = Sessao.objects.all()
    usuario_id = request.session.get('usuario_id')
    usuario = Usuario.objects.get(id=usuario_id) if usuario_id else None
    return render(request, 'usuarios/listar_sessoes.html', {'sessoes': sessoes, 'usuario': usuario})

def listar_itens(request, sessao_id):
    """
    View principal de uma sessão, listando seus itens e permitindo retiradas.

    Para GET, exibe os itens da sessão, bem como uma lista de todos os usuários
    para seleção na hora da retirada.
    Para POST, processa a retirada de um item: cria ou atualiza um registro
    de `Retirada` e debita a quantidade do estoque do `Item`.
    O acesso é protegido pela flag de sessão `sessao_{sessao.id}`.
    """
    sessao = get_object_or_404(Sessao, id=sessao_id)

    if not request.session.get(f"sessao_{sessao.id}", False):
        return redirect("listar_sessoes")

    if request.method == "POST" and 'retirar_item' in request.POST:
        item_id = request.POST.get("item_id")
        usuario_id = request.POST.get("usuario")
        quantidade = int(request.POST.get("quantidade", 1))
        item = get_object_or_404(Item, id=item_id)
        usuario = get_object_or_404(Usuario, id=usuario_id)

        if quantidade <= item.quantidade:
            retirada_existente = Retirada.objects.filter(item=item, usuario=usuario).first()

            if retirada_existente:
                retirada_existente.quantidade += quantidade
                retirada_existente.save()
            else:
              Retirada.objects.create(
                item=item,
                usuario=usuario,
                quantidade=quantidade
            )

            item.quantidade -= quantidade
            item.save()
        else:
            messages.error(request, "Quantidade solicitada maior que disponível.")
        return redirect("listar_itens", sessao_id=sessao.id)

    itens = sessao.itens.all()
    usuarios = Usuario.objects.all()
    return render(request, "usuarios/listar_itens.html", {
        "sessao": sessao,
        "itens": itens,
        "usuarios": usuarios
    })

from django.http import JsonResponse
from django.urls import reverse

def validar_sessao(request, sessao_id):
    """
    Endpoint AJAX para validar a senha de uma sessão de forma assíncrona.

    Recebe um POST com a senha e retorna um JSON indicando sucesso ou falha.
    Se a senha for válida, define a flag de autorização na sessão do usuário
    e retorna a URL de redirecionamento para a lista de itens.
    """
    if request.method == "POST":
        sessao = get_object_or_404(Sessao, id=sessao_id)
        senha = request.POST.get("senha")

        if senha == sessao.senha:
            request.session[f"sessao_{sessao.id}"] = True  

            return JsonResponse({
                "success": True,
                "redirect_url": reverse("listar_itens", args=[sessao.id])
            })
        else:
            return JsonResponse({
                "success": False,
                "error": "Senha incorreta!"
            })

    return JsonResponse({"success": False, "error": "Método inválido."}, status=400)

def retirar_item(request, item_id):
    """
    Processa a retirada de um item, exigindo confirmação por PIN do usuário.

    Recebe um POST com o ID do usuário, a quantidade e o PIN de confirmação.
    Se o PIN corresponder ao do usuário, a retirada é registrada e o estoque
    do item é atualizado. Caso contrário, uma mensagem de erro é exibida.
    """
    item = get_object_or_404(Item, id=item_id)

    if request.method == "POST":
        usuario_id = request.POST.get("usuario")
        quantidade = int(request.POST.get("quantidade", 1))
        pin_confirmacao = request.POST.get("pin_confirmacao")

        usuario = get_object_or_404(Usuario, id=usuario_id)

        if not pin_confirmacao or pin_confirmacao != usuario.pin:
            messages.error(request, f"PIN incorreto para {usuario.nome}. A retirada não foi autorizada.")
            return redirect("listar_itens", sessao_id=item.sessao.id)

        if quantidade <= item.quantidade:
            retirada_existente = Retirada.objects.filter(item=item, usuario=usuario).first()

            if retirada_existente:
                retirada_existente.quantidade += quantidade
                retirada_existente.save()
            else:
                Retirada.objects.create(
                    item=item,
                    usuario=usuario,
                    quantidade=quantidade,
                    data_retirada=timezone.now()
                )

            item.quantidade -= quantidade
            item.save()
            messages.success(request, f"Retirada registrada com sucesso para {usuario.nome}.")
        else:
            messages.error(request, "Quantidade solicitada maior que disponível.")

        return redirect("listar_itens", sessao_id=item.sessao.id)

def remover_retirada(request, retirada_id):
    """
    Reverte uma retirada, devolvendo a quantidade ao estoque do item.

    Pode remover a retirada inteira ou uma quantidade parcial, dependendo do
    que for enviado no POST. Após a operação, retorna o item ao estoque e
    redireciona para a página anterior ou para a lista de itens.
    """
    retirada = get_object_or_404(Retirada, id=retirada_id)
    item = retirada.item
    if request.method == "POST":

        qtd_remover = int(request.POST.get("quantidade", retirada.quantidade))
        if qtd_remover >= retirada.quantidade:
            item.quantidade += retirada.quantidade
            item.save()
            retirada.delete()
        else:
            item.quantidade += qtd_remover
            item.save()
            retirada.quantidade -= qtd_remover
            retirada.save()
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect("listar_itens", sessao_id=item.sessao.id)


from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import Retirada

def gerar_relatorio_pdf(request, sessao_id):
    """
    Gera um relatório em PDF das cautelas (retiradas) de uma sessão.

    Renderiza um template HTML com os dados da sessão e suas retiradas,
    e usa a biblioteca xhtml2pdf para converter o HTML em um arquivo PDF,
    que é retornado como resposta para download.
    """
    sessao = get_object_or_404(Sessao, id=sessao_id)
    
    template_path = 'usuarios/relatorio_cautelas.html'
    context = {'sessao': sessao}
    
    template = get_template(template_path)
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="relatorio_sessao_{sessao.id}.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Erro ao gerar PDF")
    return response


def editar_item(request, item_id):
    """
    Renderiza e processa o formulário para editar um item existente.

    O acesso é protegido pela flag de sessão. Em caso de POST, atualiza
    o nome e a quantidade do item.
    """
    item = get_object_or_404(Item, id=item_id)
    sessao = item.sessao

    if not request.session.get(f"sessao_{sessao.id}", False):
        messages.error(request, "Você não tem permissão para editar itens nesta sessão.")
        return redirect("listar_sessoes")

    if request.method == "POST":
        nome = request.POST.get("nome")
        quantidade = int(request.POST.get("quantidade", 1))

        if nome and quantidade > 0:
            item.nome = nome
            item.quantidade = quantidade
            item.save()
            messages.success(request, f"Item '{item.nome}' atualizado com sucesso!")
            return redirect("listar_itens", sessao_id=sessao.id)
        else:
            messages.error(request, "Nome e quantidade são obrigatórios.")

    return render(request, "usuarios/editar_item.html", {"item": item})

def excluir_item(request, item_id):
    """
    Processa a exclusão de um item após confirmação.

    Para GET, exibe uma página de confirmação.
    Para POST, deleta o item do banco de dados e redireciona para a lista
    de itens da sessão correspondente.
    """
    item = get_object_or_404(Item, id=item_id)
    sessao_id = item.sessao.id
    if request.method == "POST":
        item.delete()
        return redirect("listar_itens", sessao_id=sessao_id)
    return render(request, "usuarios/confirmar_exclusao.html", {"item": item})

def admin_panel(request):
    """
    Painel de controle principal para administradores.

    Acesso restrito a usuários com a flag `is_admin`. Coleta diversas
    estatísticas sobre itens, retiradas, sessões e usuários para
    exibição em cards e gráficos no template `admin_panel.html`.
    """
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_id = request.session.get('usuario_id')
    usuario = Usuario.objects.get(id=usuario_id)
    if not usuario.is_admin:
        messages.error(request, "Acesso negado. Você não tem permissão de administrador.")
        return redirect('listar_sessoes')

    total_itens = Item.objects.count()
    total_retiradas = Retirada.objects.aggregate(total=Sum('quantidade'))['total'] or 0
    porcentagem_cautelados = (total_retiradas / total_itens * 100) if total_itens > 0 else 0

    sessoes_com_mais_retiradas = Sessao.objects.annotate(
        total_retiradas=Sum('itens__retiradas__quantidade')
    ).filter(total_retiradas__gt=0).order_by('-total_retiradas')[:5]

    item_mais_cautelado = Item.objects.annotate(
        total_retiradas=Sum('retiradas__quantidade')
    ).filter(total_retiradas__gt=0).order_by('-total_retiradas').first()

    sessoes_labels = [sessao.nome for sessao in sessoes_com_mais_retiradas]
    sessoes_data = [sessao.total_retiradas for sessao in sessoes_com_mais_retiradas]

    graduacoes = Usuario.objects.values('graduacao').annotate(count=Count('graduacao')).order_by('graduacao')
    usuarios_labels = [graduacao['graduacao'] for graduacao in graduacoes]
    usuarios_data = [graduacao['count'] for graduacao in graduacoes]

    itens_por_sessao = Sessao.objects.annotate(total_itens=Count('itens')).values('nome', 'total_itens')
    itens_sessao_labels = [sessao['nome'] for sessao in itens_por_sessao]
    itens_sessao_data = [sessao['total_itens'] for sessao in itens_por_sessao]

    context = {
        'total_itens': total_itens,
        'total_retiradas': total_retiradas,
        'porcentagem_cautelados': round(porcentagem_cautelados, 2),
        'sessoes_com_mais_retiradas': sessoes_com_mais_retiradas,
        'item_mais_cautelado': item_mais_cautelado,
        'sessoes_labels': sessoes_labels,
        'sessoes_data': sessoes_data,
        'usuarios_labels': usuarios_labels,
        'usuarios_data': usuarios_data,
        'itens_sessao_labels': itens_sessao_labels,
        'itens_sessao_data': itens_sessao_data,
        'usuarios': Usuario.objects.all(),
        'sessoes': Sessao.objects.all(),
    }
    return render(request, 'usuarios/admin_panel.html', context)


def editar_usuario(request, usuario_id):
    """
    Renderiza e processa o formulário de edição de um usuário.

    Acesso restrito a administradores. Para GET, exibe o formulário
    `UsuarioEditForm` preenchido com os dados do usuário. Para POST,
    salva as alterações.
    """
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_logado = Usuario.objects.get(id=request.session['usuario_id'])
    if not usuario_logado.is_admin:
        messages.error(request, "Acesso negado. Você não tem permissão de administrador.")
        return redirect('listar_sessoes')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuário {usuario.nome} atualizado com sucesso!')
            return redirect('admin_panel')
    else:
        form = UsuarioEditForm(instance=usuario)

    return render(request, 'usuarios/editar_usuario.html', {
        'form': form,
        'usuario': usuario
    })


def excluir_usuario(request, usuario_id):
    """
    Processa a exclusão de um usuário após confirmação.

    Acesso restrito a administradores. Para GET, mostra uma página de
    confirmação. Para POST, deleta o usuário e redireciona para o painel de admin.
    """
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_logado = Usuario.objects.get(id=request.session['usuario_id'])
    if not usuario_logado.is_admin:
        messages.error(request, "Acesso negado. Você não tem permissão de administrador.")
        return redirect('listar_sessoes')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, f'Usuário {usuario.nome} excluído com sucesso!')
        return redirect('admin_panel')

    return render(request, 'usuarios/confirmar_exclusao_usuario.html', {
        'usuario': usuario
    })


def excluir_usuario_ajax(request):
    """
    Endpoint AJAX para excluir um usuário de forma assíncrona.

    Acesso restrito a administradores. Recebe um POST com o `usuario_id`,
    deleta o usuário e retorna uma resposta JSON com status de sucesso.
    """
    if request.method == 'POST':
        if 'usuario_id' not in request.session:
            return JsonResponse({'success': False, 'error': 'Não autorizado'})
        usuario_logado = Usuario.objects.get(id=request.session['usuario_id'])
        if not usuario_logado.is_admin:
            return JsonResponse({'success': False, 'error': 'Acesso negado'})

        usuario_id = request.POST.get('usuario_id')
        usuario = get_object_or_404(Usuario, id=usuario_id)
        usuario.delete()
        return JsonResponse({'success': True, 'message': f'Usuário {usuario.nome} excluído com sucesso!'})

    return JsonResponse({'success': False, 'error': 'Método inválido'})

def excluir_sessao_ajax(request):
    """
    Endpoint AJAX para excluir uma sessão de forma assíncrona.

    Acesso restrito a administradores. Recebe um POST com o `sessao_id`,
    deleta a sessão e retorna uma resposta JSON com status de sucesso.
    """
    if request.method == 'POST':
        if 'usuario_id' not in request.session:
            return JsonResponse({'success': False, 'error': 'Não autorizado'})
        usuario_logado = Usuario.objects.get(id=request.session['usuario_id'])
        if not usuario_logado.is_admin:
            return JsonResponse({'success': False, 'error': 'Acesso negado'})

        sessao_id = request.POST.get('sessao_id')
        sessao = get_object_or_404(Sessao, id=sessao_id)
        sessao.delete()
        return JsonResponse({'success': True, 'message': f'Sessão {sessao.nome} excluída com sucesso!'})

    return JsonResponse({'success': False, 'error': 'Método inválido'})

def editar_sessao(request, sessao_id):
    """
    Renderiza e processa o formulário para editar uma sessão existente.

    Acesso restrito a administradores. Para GET, exibe um formulário para
    alterar o nome e a senha da sessão. Para POST, salva as alterações.
    """
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_logado = Usuario.objects.get(id=request.session['usuario_id'])
    if not usuario_logado.is_admin:
        messages.error(request, "Acesso negado. Você não tem permissão de administrador.")
        return redirect('listar_sessoes')

    sessao = get_object_or_404(Sessao, id=sessao_id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')

        if nome and senha:
            sessao.nome = nome
            sessao.senha = senha
            sessao.save()
            messages.success(request, f'Sessão {sessao.nome} atualizada com sucesso!')
            return redirect('admin_panel')
        else:
            messages.error(request, "Nome e senha são obrigatórios.")

    return render(request, 'usuarios/editar_sessao.html', {
        'sessao': sessao
    })


def excluir_sessao(request, sessao_id):
    """
    Processa a exclusão de uma sessão após confirmação.

    Acesso restrito a administradores. Para GET, mostra uma página de
    confirmação. Para POST, deleta a sessão e redireciona para o painel de admin.
    """
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_logado = Usuario.objects.get(id=request.session['usuario_id'])
    if not usuario_logado.is_admin:
        messages.error(request, "Acesso negado. Você não tem permissão de administrador.")
        return redirect('listar_sessoes')

    sessao = get_object_or_404(Sessao, id=sessao_id)

    if request.method == 'POST':
        sessao.delete()
        messages.success(request, f'Sessão {sessao.nome} excluída com sucesso!')
        return redirect('admin_panel')

    return render(request, 'usuarios/confirmar_exclusao_sessao.html', {
        'sessao': sessao
    })
    