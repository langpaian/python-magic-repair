def new_box(owner, coins=None):
    if coins is None:
        coins = []
    coins.append(owner)
    return coins
