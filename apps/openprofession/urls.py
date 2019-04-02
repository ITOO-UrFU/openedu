from django.conf.urls import url
from graphene_django.views import GraphQLView
from .views import entry, entry_list, add_entry, add_pd, ReportUploadView, personal_data_list, thanks, updatePD, \
    add_sim_data, sim_thanks, add_seminar_bid, seminar_thanks, add_epd

urlpatterns = [
    url(r'^(?P<pk>\d+)$', entry, name="entry"),
    url(r'^$', entry_list, name="entry_list"),
    url(r'^add_entry/$', add_entry, name="add_entry"),

    url(r'^new/$', add_pd, name="add_personal_data"),
    url(r'^edcrunch_new/$', add_epd, name="add_edcrunch_personal_data"),
    url(r'^new_sim/$', add_sim_data, name="add_sim_data"),
    url(r'^list/$', personal_data_list, name="personal_data_list"),
    url(r'^update/$', updatePD, name="updatePD"),
    url(r'^thanks/$', thanks, name="thanks"),
    url(r'^edthanks/$', edthanks, name="edthanks"),
    url(r'^sim_thanks/$', sim_thanks, name="sim_thanks"),
    url(r'^upload/$', ReportUploadView.as_view(), name="upload_reports"),
    url(r'^graphql', GraphQLView.as_view(graphiql=True)),
    # url(r'^test/', set_program_grade, name="set_program_grade"),

    ## запись на семинар
    url(r'^seminar/$', add_seminar_bid, name="add_seminar_bid"),
    url(r'^seminar_thanks/$', seminar_thanks, name="seminar_thanks"),
]
