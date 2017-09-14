from connection import connection, com_switch, Database
from client.step_body import StepBody
from data_config import CaseSteps, StepData


class Steps:
    def __init__(self):
        pass

    def __contains__(self, item):
        return len(StepBody.search(item)) > 0

    @staticmethod
    def cache_step(step_id):
        """
        Decode data from connection to steps that can by displayed on UI

        There should by a delate to coresponding comment.
        :param step_id:
        :return:
        """
        if step_id in StepBody.steps_ids:
            return StepBody.STEPS.get(step_id)
        else:
            step_body_dict = connection.get_step(step_id)
            if step_body_dict is not None:
                if str(step_body_dict.get(StepData.IS_ACTIVE)) == "true":
                    return StepBody(step_body_dict)
                else:
                    return None
            else:
                return None

    @staticmethod
    def case_steps(request):
        """
        Create sorted list of steps bound to case in rising order.
        :param request:
        :return:
        """
        print(request)
        ret_val = []
        for data_step in request:
            step_id = str(data_step.get(CaseSteps.STEP_ID, 0))
            step_body = Steps.cache_step(step_id)
            if step_body is not None:
                ret_val.append(step_body)
        return ret_val


if __name__ == '__main__':
    connection = Database()

    steps_order = connection.get_steps(1)
    items = Steps.case_steps(steps_order)

    print("items {}".format(items))
