from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('reg_developer',views.reg_developer,name='reg_developer'),
    path('reg_TL',views.reg_TL,name='reg_TL'),
    path('loginhome',views.loginhome,name='loginhome'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('TL_home',views.TL_home,name='TL_home'),
    path('register_TL',views.register_TL,name='register_TL'),
    path('register_dev',views.register_dev,name='register_dev'),
    path('ulogin',views.ulogin,name='ulogin'),
    path('view_tl',views.view_tl,name='view_tl'),
    path('view_developer',views.view_developer,name='view_developer'),
    path('view_project',views.view_project,name='view_project'),
    path('tl_pworkprogress',views.tl_pworkprogress,name='tl_pworkprogress'),
    path('admin_module/<int:id>',views.admin_module,name='admin_module'),
    path('admin_mprogress/<int:id>',views.admin_mprogress,name='admin_mprogress'),
    path('dev_modules',views.dev_modules,name='dev_modules'),
    path('change_member/<int:pk>/<int:upk>/',views.change_member,name='change_member'),
    path('change_developer/<int:pk>',views.change_developer,name='change_developer'),
    path('assign_project',views.assign_project,name='assign_project'),
    path('add_project',views.add_project,name='add_project'),
    path('add_modulefun',views.add_modulefun,name='add_modulefun'),
    path('calendar/<int:id>/<int:tlid>/',views.calendar,name='calendar'),
    path('tl_ppworkprogress/<int:id>',views.tl_ppworkprogress,name='tl_ppworkprogress'),
    path('dev_viewprogress/<int:id>',views.dev_viewprogress,name='dev_viewprogress'),
    path('tl_devpro/<int:id>',views.tl_devpro,name='tl_devpro'),
    path('adminworkprogress',views.adminworkprogress,name='adminworkprogress'),
    path('progress/<int:id>',views.progress,name='progress'),
    path('progresspro/<int:id>',views.progresspro,name='progresspro'),
    path('tl_progressmod/<int:id>',views.tl_progressmod,name='tl_progressmod'),
    path('tl_devpro/<int:id>',views.tl_devpro,name='tl_devpro'),

    path('progresspr/<int:id>',views.progresspr,name='progresspr'),
    path('print_dates/<int:start_date>/<int:end_date>/',views.print_dates,name='print_dates'),
    path('pemployee',views.pemployee,name='pemployee'),
    path('admin_viewproject',views.admin_viewproject,name='admin_viewproject'),
    path('TLworkprogress',views.TLworkprogress,name='TLworkprogress'),
    path('TL_updateworkprogress/<int:id>',views.TL_updateworkprogress,name='TL_updateworkprogress'),
    path('project_updatefun/<int:id>',views.project_updatefun,name='project_updatefun'),
    path('new_member',views.new_member,name='new_member'),
    path('open_certificate/<int:id>',views.open_certificate,name='open_certificate'),
    path('open_Pprogress/<int:id>',views.open_Pprogress,name='open_Pprogress'),
    path('open_mprogress/<int:id>',views.open_mprogress,name='open_mprogress'),
    path('open_project/<int:id>',views.open_project,name='open_project'),
    path('project_updatefun/<int:id>',views.project_updatefun,name='project_updatefun'),    
    path('open_attachment/<int:id>',views.open_attachment,name='open_attachment'),
    path('open_attachment/<int:id>',views.open_attachment,name='open_attachment'),
    path('view_moduledev/<int:id>',views.view_moduledev,name='view_moduledev'),
    path('approve/<int:id>',views.approve,name='approve'),
    path('reject/<int:id>',views.reject,name='reject'),

    # path('enddate',views.enddate,name='enddate'),
    path('waiting',views.waiting,name='waiting'),
    path('assign_TL/<int:id>',views.assign_TL,name='assign_TL'),
    path('assignfun/<int:id>',views.assignfun,name='assignfun'),
    path('viewdeveloper_TL',views.viewdeveloper_TL,name='viewdeveloper_TL'),
    path('add_module',views.add_module,name='add_module'),

    path('assign_module',views.assign_module,name='assign_module'),
    
    path('updatework/<int:id>',views.updatework,name='updatework'),
    path('editworkfun/<int:id>',views.editworkfun,name='editworkfun'),
    path('editfun_dev/<int:id>',views.editfun_dev,name='editfun_dev'),

    # path('TLenddate',views.TLenddate,name='TLenddate'),
    # path('TL_module_end',views.TL_module_end,name='TL_module_end'),
    path('TL_change_pwd',views.TL_change_pwd,name='TL_change_pwd'),
    path('dev_change_pwd',views.dev_change_pwd,name='dev_change_pwd'),

    path('custom_password_change_view',views.custom_password_change_view,name='custom_password_change_view'),
    path('dev_password_change_view',views.dev_password_change_view,name='dev_password_change_view'),

    path('dev_home',views.dev_home,name='dev_home'),
    path('dev_viewmodule',views.dev_viewmodule,name='dev_viewmodule'),
    path('dev_updatework',views.dev_updatework,name='dev_updatework'),
    # path('dev_enddate',views.dev_enddate,name='dev_enddate'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('TL_logout',views.TL_logout,name='TL_logout'),
    path('dev_logout',views.dev_logout,name='dev_logout'),
    path('update_dev/<int:id>',views.update_dev,name='update_dev'),
    path('TL_profile',views.TL_profile,name='TL_profile'),
    path('dev_profile',views.dev_profile,name='dev_profile'),
    path('assign_teamleader',views.assign_teamleader,name='assign_teamleader'),
    path('tl_assign',views.tl_assign,name='tl_assign'),
    path('tldev_assign/<int:id>',views.tldev_assign,name='tldev_assign'),

    path('deletetl/<int:id>',views.deletetl,name='deletetl'),
    path('deletedev/<int:id>',views.deletedev,name='deletedev'),
    path('TLprofile_edit/<int:id>',views.TLprofile_edit,name='TLprofile_edit'),
    path('devprofile_edit/<int:id>',views.devprofile_edit,name='devprofile_edit'),
    path('edit_tl/<int:id>',views.edit_tl,name='edit_tl'),
    path('edit_dev/<int:id>',views.edit_dev,name='edit_dev'),
    path('proj_assignfun',views.proj_assignfun,name='proj_assignfun'),
    path('mod_assignfun',views.mod_assignfun,name='mod_assignfun'),
    path('client_profile/<int:id>',views.client_profile,name='client_profile'),
    path('tl_project/<int:id>',views.tl_project,name='tl_project'),

    path('TL_viewmodules',views.TL_viewmodules,name='TL_viewmodules'),
    path('TL_assignmodule',views.TL_assignmodule,name='TL_assignmodule'),










    


    

















]