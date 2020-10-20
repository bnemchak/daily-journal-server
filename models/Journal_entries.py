class Journal_entries():
    def __init__(self, id, concept, entry, mood_id, date):
        self.id = id
        self.concept = concept
        self.entry = entry
        self.mood_id = mood_id
        self.date = date
        self.mood = None

    def __repr__(self):
        return (f"id: {self.id}")
