from connection import connection
from client.step_body import StepBody
from data_config import CaseSteps, StepData


class Steps:
    def __init__(self):
        pass

    def search(self, finder):
        return [StepBody.STEPS[step] for step in StepBody.STEPS.keys() if StepBody.STEPS[step].match(finder)]

    def __contains__(self, item):
        return len(self.search(item)) > 0

    def cache_step(self, step_id):
        """
        Decode data from serwer to steps that can by displayed on UI

        There should by a delate to coresponding comment.
        :param step_id:
        :return:
        """
        if step_id in StepBody:
            return StepBody.STEPS.get(step_id)
        else:
            items = connection.get_step(step_id)
            if len(items) > 0:
                if str(items.get(StepData.IS_ACTIVE)) == "1":
                    return StepBody(items)
                else:
                    return None
            else:
                return None

    def case_steps(self, request):
        print(request)
        ret_val = []
        for data_step in request:
            step_id = str(data_step.get(CaseSteps.STEP_ID, 0))
            step_body = self.cache_step(step_id)
            if step_body is not None:
                ret_val.append(step_body)
        return ret_val
