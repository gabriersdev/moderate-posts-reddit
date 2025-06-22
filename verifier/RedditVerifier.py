def _posts_has_moderated(item):
  reasons = [
    item.approved,
    item.removed,
    item.selftext == "[deleted]",
    item.removed_by_category == "deleted"
  ]

  exists_true = [i for i in reasons if i == True]
  exists_true = len(exists_true) >= 1 and exists_true[0] == True

  return exists_true


def verify(item):
  return _posts_has_moderated(item)
