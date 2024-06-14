from fastf1 import get_event_schedule, get_event
from cache import Cache

class Manager:     
    def _handle_tr(self, text: str):
        result = str(text).split(" ")
        return "_".join(result)
    @Cache().cache
    def get_event(self, year: int):
        gp_s = {"Country": []}
        event = get_event_schedule(year=year)
        lengh = len(event.RoundNumber.to_list())

        for i in range(1, lengh):
            gp_s["Country"].append(
                {
                    "t": event.EventName[i],
                    "tr": self._handle_tr(event.EventName[i]),
                    "round_num": i,
                    "location": event.Location[i],
                }
            )

        return gp_s
    @Cache().cache
    def get_session(self, year: int, country: str):
        event = get_event(year=year, gp=country)
        sessions = {"sessions": []}
        i = []
        num = 1
        while True:
            try:
                session = event[f"Session{num}"]
                i.append(session)
                num += 1
            except:
                break
        for session in i:
            sessions["sessions"].append(self._handle_tr(session))

        return sessions
# s = Manager()
# d = s.get_event(year=2018)
# print(d)