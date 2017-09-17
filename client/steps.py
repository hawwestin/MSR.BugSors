from collections import UserList

from client.step_body import StepBody
from client.connection_module import com_switch, Database
from client.data_config import CaseSteps, StepData


class Steps(list):
    """
    Keep order of step that are bound to Test Case.
    """

    def __setitem__(self, key, value):
        if value in self:
            raise ValueError("cannot repeat steps")
        super().__setitem__(key, value)

    def insert(self, index, object):
        if object in self:
            raise ValueError("Cannot repeat steps")
        super().insert(index, object)

    def append(self, object):
        if object in self:
            raise ValueError("Cannot repeat steps")
        super().append(object)

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
            step_body_dict = com_switch.connection.get_step(step_id)
            if step_body_dict is not None:
                if str(step_body_dict.get(StepData.IS_ACTIVE)) == "true":
                    return StepBody(step_body_dict)
                else:
                    return None
            else:
                return None

    def get_steps(self) -> list:
        """
        From self ordered list of steps return theirs objects.
        :param steps_ids: steps ids
        :return: list of StepBody objects
        """
        ret_val = []
        for step_id in self:
            step_body = Steps.cache_step(step_id)
            if step_body is not None:
                ret_val.append(step_body)

        return ret_val

    def sort_case_steps(self, request):
        """
        Create sorted list of steps bound to case in rising order.
        :param request:
        :return:
        """
        self.clear()
        #  todo error with repeated step_id. use record id somehow

        for row in range(len(request)):
            data_step = request[row]
            prev_step_id = str(data_step.get(CaseSteps.PREVIOUS_STEP_ID, 0))
            step_id = str(data_step.get(CaseSteps.STEP_ID, 0))
            # identify first step
            if prev_step_id is None:
                if len(self) == 0:
                    self.append(step_id)
                else:
                    self.insert(0, step_id)
            # regular step insert
            else:
                # find previous
                if prev_step_id in self:
                    self.insert(int(self.index(prev_step_id)) + 1, step_id)
                else:
                    self.append(step_id)
                    # todo debug logger ("order {}".format(self))
        return self.get_steps()


if __name__ == '__main__':
    com_switch.connection = Database()
    steps = Steps()
    steps_order = com_switch.connection.get_steps(3)
    items = steps.sort_case_steps(steps_order)
    print("order {}".format(steps))
    print("items {}".format(items))
