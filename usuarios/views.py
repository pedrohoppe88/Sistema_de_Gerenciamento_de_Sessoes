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
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # Aqui você poderia hash a senha se quiser
            form.save()
            return redirect('login')
           # return redirect('sucesso')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/cadastrar.html', {
        'form': form,
        'graduacao_choices': Usuario.GRADUACAO_CHOICES
    })

def sucesso(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    usuario_id = request.session.get('usuario_id')
    usuario = Usuario.objects.get(id=usuario_id) if usuario_id else None
    nome = usuario.nome if usuario else None
    graduacao = usuario.graduacao if usuario else None
    return render(request, 'usuarios/sucesso.html', {'usuario_id': usuario_id, 'graduacao': graduacao, 'nome': nome})

def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            try:
                usuario = Usuario.objects.get(email=email)
                if check_password(senha, usuario.senha):
                    request.session['usuario_id'] = usuario.id  # salva sessão
                    return redirect('sucesso')
                else:
                    form.add_error('senha', 'Senha incorreta.')
            except Usuario.DoesNotExist:
                form.add_error('email', 'Usuário não encontrado.')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_usuario(request):
    request.session.flush()  # remove todas as sessões
    return redirect('login')

def listar_usuarios(request):
    if 'usuario_id' not in request.session:
        return redirect('login')  # protege a página
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/all_users.html', {'usuarios': usuarios})

def all_users(request):
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
    if 'usuario_id' not in request.session:
        return redirect('login')  # protege a página

    usuarios = Usuario.objects.all()

    # Contagem para os cards de estatísticas
    total_usuarios = usuarios.count()
    usuarios_ativos = usuarios.filter(status='ativo').count()  # se você tiver campo status
    graduados_recentes = usuarios.order_by('-id')[:5].count()  # últimos 5 cadastrados

    context = {
        'usuarios': usuarios,
        'total_usuarios': total_usuarios,
        'usuarios_ativos': usuarios_ativos,
        'graduados_recentes': graduados_recentes,
    }
    
    
def entrar_sessao(request, sessao_id):
    sessao = get_object_or_404(Sessao, id=sessao_id)
    
    if request.method  == "POST":
        senha = request.POST.get('senha')
        if sessao.senha == senha:
            request.session[f"sessao_{sessao.id}"] = True;
            return redirect('detalhes_sessao', sessao_id=sessao.id)
        else:
            messages.error(request, 'Senha incorreta.')
            return render(request, "entrar_sessao.html", {"sessao": sessao})
    
def detalhes_sessao(request, sessao_id):
    sessao = get_object_or_404(Sessao, id=sessao_id)

    # Só entra se for admin ou se tiver a senha
    if not request.user == sessao.criador and not request.session.get(f"sessao_{sessao.id}", False):
        messages.error(request, "Acesso negado!")
        return redirect("entrar_sessao", sessao_id=sessao.id)

    itens = sessao.itens.all()
    return render(request, "detalhes_sessao.html", {"sessao": sessao, "itens": itens})

def adicionar_item(request, sessao_id):
    sessao = get_object_or_404(Sessao, id=sessao_id)

    # Proteção: só o criador ou quem entrou na sessão pode adicionar
    if not request.user == sessao.criador and not request.session.get(f"sessao_{sessao.id}", False):
        messages.error(request, "Você não tem permissão!")
        return redirect("entrar_sessao", sessao_id=sessao.id)

    if request.method == "POST":
        nome = request.POST.get("nome")
        quantidade = int(request.POST.get("quantidade", 1))
        Item.objects.create(sessao=sessao, nome=nome, quantidade=quantidade)

        # 🔹 Redireciona de volta para a página de itens
        return redirect("listar_itens", sessao_id=sessao.id)

    # Se precisar de template separado (não usado no modal)
    return render(request, "adicionar_item.html", {"sessao": sessao})

"""
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # Aqui você poderia hash a senha se quiser
            form.save()
            return redirect('login')
           # return redirect('sucesso')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/cadastrar.html', {'form': form})

-------------------------------

def criar_sessao(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    if request.method == "POST":
        nome = request.POST.get("nome")
        senha = request.POST.get("senha")

        if Sessao.objects.filter(nome=nome).exists():
            messages.error(request, "Já existe uma sessão com esse nome.")
        else:
            Sessao.objects.create(nome=nome, senha=senha, criador=request.user)
            messages.success(request, "Sessão criada com sucesso!")
            return redirect("listar_sessoes")

    return render(request, "usuarios/criar_sessao.html")


"""

def criar_sessao(request):
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
    usuario_id = request.session.get('usuario_id')
    return HttpResponse(f"Usuário logado (usuario_id): {usuario_id}")

def listar_sessoes(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    sessoes = Sessao.objects.all()
    usuario_id = request.session.get('usuario_id')
    usuario = Usuario.objects.get(id=usuario_id) if usuario_id else None
    return render(request, 'usuarios/listar_sessoes.html', {'sessoes': sessoes, 'usuario': usuario})

def listar_itens(request, sessao_id):
    sessao = get_object_or_404(Sessao, id=sessao_id)

    if not request.session.get(f"sessao_{sessao.id}", False):
        return redirect("listar_sessoes")

    # Processa retirada se for POST (chama a lógica de retirar_item)
    if request.method == "POST" and 'retirar_item' in request.POST:
        item_id = request.POST.get("item_id")
        usuario_id = request.POST.get("usuario")
        quantidade = int(request.POST.get("quantidade", 1))
        item = get_object_or_404(Item, id=item_id)
        usuario = get_object_or_404(Usuario, id=usuario_id)

        if quantidade <= item.quantidade:
            # Verifica se já existe retirada para o mesmo usuário + item
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

            # Atualiza estoque
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
    if request.method == "POST":
        sessao = get_object_or_404(Sessao, id=sessao_id)
        senha = request.POST.get("senha")

        if senha == sessao.senha:  # ⚠️ use hash em produção
            # salva login na sessão do usuário
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
    item = get_object_or_404(Item, id=item_id)

    if request.method == "POST":
        usuario_id = request.POST.get("usuario")
        quantidade = int(request.POST.get("quantidade", 1))
        pin_confirmacao = request.POST.get("pin_confirmacao")

        usuario = get_object_or_404(Usuario, id=usuario_id)

        # Verificar PIN obrigatório do usuário selecionado
        if not pin_confirmacao or pin_confirmacao != usuario.pin:
            messages.error(request, f"PIN incorreto para {usuario.nome}. A retirada não foi autorizada.")
            return redirect("listar_itens", sessao_id=item.sessao.id)

        if quantidade <= item.quantidade:
            # Verifica se já existe retirada para o mesmo usuário + item
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

            # Atualiza estoque
            item.quantidade -= quantidade
            item.save()
            messages.success(request, f"Retirada registrada com sucesso para {usuario.nome}.")
        else:
            messages.error(request, "Quantidade solicitada maior que disponível.")

        return redirect("listar_itens", sessao_id=item.sessao.id)

def remover_retirada(request, retirada_id):
    retirada = get_object_or_404(Retirada, id=retirada_id)
    item = retirada.item
    if request.method == "POST":

        qtd_remover = int(request.POST.get("quantidade", retirada.quantidade))
        if qtd_remover >= retirada.quantidade:
            item.quantidade += retirada.quantidade
            item.save()
            retirada.delete()
        else:
            # Remove apenas parte da retirada
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
    item = get_object_or_404(Item, id=item_id)
    sessao = item.sessao

    # Verificar se o usuário tem acesso à sessão
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
    item = get_object_or_404(Item, id=item_id)
    sessao_id = item.sessao.id  # Salva o ID da sessão antes de excluir o item
    if request.method == "POST":
        item.delete()
        return redirect("listar_itens", sessao_id=sessao_id)  # Redireciona usando o ID salvo
    return render(request, "usuarios/confirmar_exclusao.html", {"item": item})

def admin_panel(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_id = request.session.get('usuario_id')
    usuario = Usuario.objects.get(id=usuario_id)
    if not usuario.is_admin:
        messages.error(request, "Acesso negado. Você não tem permissão de administrador.")
        return redirect('listar_sessoes')

    # Estatísticas gerais
    total_itens = Item.objects.count()
    total_retiradas = Retirada.objects.aggregate(total=Sum('quantidade'))['total'] or 0
    porcentagem_cautelados = (total_retiradas / total_itens * 100) if total_itens > 0 else 0

    # Sessões com mais retiradas
    sessoes_com_mais_retiradas = Sessao.objects.annotate(
        total_retiradas=Sum('itens__retiradas__quantidade')
    ).filter(total_retiradas__gt=0).order_by('-total_retiradas')[:5]

    # Item mais cautelado
    item_mais_cautelado = Item.objects.annotate(
        total_retiradas=Sum('retiradas__quantidade')
    ).filter(total_retiradas__gt=0).order_by('-total_retiradas').first()

    # Dados para gráficos
    sessoes_labels = [sessao.nome for sessao in sessoes_com_mais_retiradas]
    sessoes_data = [sessao.total_retiradas for sessao in sessoes_com_mais_retiradas]

    # Dados para gráfico de usuários por graduação
    graduacoes = Usuario.objects.values('graduacao').annotate(count=Count('graduacao')).order_by('graduacao')
    usuarios_labels = [graduacao['graduacao'] for graduacao in graduacoes]
    usuarios_data = [graduacao['count'] for graduacao in graduacoes]

    # Dados para gráfico de itens por sessão
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
