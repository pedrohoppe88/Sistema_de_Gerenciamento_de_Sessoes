from django.urls import path
from . import views

urlpatterns = [
    path('all_users/', views.all_users, name='all_users'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path("criar_sessao/", views.criar_sessao, name="criar_sessao"),
    path('listar_sessoes/', views.listar_sessoes, name='listar_sessoes'),
    path('usuarios/<int:sessao_id>/itens/', views.listar_itens, name='listar_itens'),
    path("sessao/<int:sessao_id>/adicionar_item/", views.adicionar_item, name="adicionar_item"),
    path('item/<int:item_id>/retirar/', views.retirar_item, name='retirar_item'),
    path('retirada/<int:retirada_id>/remover/', views.remover_retirada, name='remover_retirada'),
    path('sessao/<int:sessao_id>/itens/relatorio/pdf/', views.gerar_relatorio_pdf, name='gerar_relatorio_pdf'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('editar_usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('excluir_usuario_ajax/', views.excluir_usuario_ajax, name='excluir_usuario_ajax'),
    path('excluir_sessao/<int:sessao_id>/', views.excluir_sessao, name='excluir_sessao'),
    path('editar_sessao/<int:sessao_id>/', views.editar_sessao, name='editar_sessao'),
    path('excluir_usuario/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
    
]
