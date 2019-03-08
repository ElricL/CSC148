class Runner:
    """a runner class

    === attributes ===
    name: the name of runner
    email address: runner's email
    speed category: how fast runner can go
    """

    name: str
    email_address: str
    speed_category: str

    def __init__(self, name: str, email: str, speed_category: str) -> None:
        """initialize a runner entry

        """
        self.name = name
        self.email = email
        self.speed_category = speed_category

    def edit_email(self, new_email: str) -> None:
        """Edit runner's email into new email

        """
        self.email = new_email

    def edit_speed(self, new_category: str) -> None:
        """Edit runner's speed category

        """
        self.speed_category = new_category


class Registry:
    """Registry Class"""
    runners: dict

    def __init__(self) -> None:
        self.runners = {}

    def add_runner(self, runner_name: str, email_address: str, category: str) -> None:
        """add runner to registry
        """

        new_runner = Runner(runner_name, email_address, category)
        if category not in self.runners:
            self.runners[category] = [new_runner]
        else:
            self.runners[category].append(new_runner)

    def report_category(self, category):
        if category in self.runners:
            runner_list = []
            for registrant in self.runners[category]:
                runner_list.append(registrant.name)
            return runner_list
        else:
            return 'No runners in ' + category + ' category'

    def runner_speed(self, runner: str) -> str:
        '''find speed category of runner identified
        '''
        for category in self.runners:
            for registrant in self.runners[category]:
                if registrant.name == runner:
                    return category

    def withdraw_runner(self, runner: str) -> None:
        for category in self.runners:
            for registrant in self.runners[category]:
                if registrant.name == runner:
                    self.runners[category].remove(registrant)

    def change_category(self, runner_name: str, new_category: str) -> None:
        for category in self.runners:
            for registrant in self.runners[category]:
                if registrant.name == runner_name:
                    registrant.edit_speed(new_category)
                    if new_category in self.runners:
                        self.withdraw_runner(runner_name)
                        self.runners[new_category].append(registrant)
                    else:
                        self.withdraw_runner(runner_name)
                        self.runners[new_category] = [registrant]

if __name__ == '__main__':
    registry = Registry()
    registry.add_runner('Gerhard', 'Gerhard@hotmail.com', 'Under 40 mins')
    registry.add_runner('Tom', 'Tom@hotmail.com', 'Under 30 mins')
    registry.add_runner('Toni', 'Toni@hotmail.com', 'Under 20 mins')
    registry.add_runner('Margot', 'Margot@hotmail.com', 'Under 30 mins')
    print(registry.report_category('Under 30 mins'))
    registry.change_category('Gerhard', 'Under 30 mins')
    print(registry.report_category('Under 30 mins'))
