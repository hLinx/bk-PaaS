# -*- coding: utf-8 -*-
from django import forms

from common.forms import BaseComponentForm
from components.component import Component
from common.constants import API_TYPE_Q, HTTP_METHOD

from .toolkit import tools, configs


class GetJobInstanceLog(Component):
    suggest_method = HTTP_METHOD.GET
    label = u"根据作业实例ID查询作业执行日志"
    label_en = "Get job instance log"

    sys_name = configs.SYSTEM_NAME
    api_type = API_TYPE_Q

    host = configs.host

    class Form(BaseComponentForm):
        bk_biz_id = forms.IntegerField(label="business id", required=True)
        job_instance_id = forms.IntegerField(label="job instance id", required=True)
        use_html_encode = forms.BooleanField(label="use html encode", required=False)

        def clean(self):
            data = self.cleaned_data
            params_keys = [
                "job_instance_id",
                "use_html_encode",
            ]
            return {
                "bk_biz_id": data["bk_biz_id"],
                "params": self.get_cleaned_data_when_exist(keys=params_keys),
            }

    def handle(self):
        params = tools.get_action_params(
            action="get_job_instance_log",
            params=self.form_data,
            operator=self.current_user.username,
            app_code=self.request.app_code,
            request_id=self.request.request_id,
        )

        client = tools.JOBClient(self.outgoing.http_client)
        self.response.payload = client.post(
            self.host, "/api/v2/get_job_instance_log", data=params, bk_language=self.request.bk_language
        )