import pandas as pd


def load_customer_data():
    """
    Load the additional e-commerce datasets.
    """

    data = {}

    files = {
        "interactions": "data/interactions.csv",
        "purchases": "data/purchases.csv",
        "reviews": "data/reviews.csv",
        "sessions": "data/sessions.csv",
        "users": "data/users.csv"
    }

    for name, file_path in files.items():

        try:

            data[name] = pd.read_csv(
                file_path
            )

        except FileNotFoundError:

            data[name] = pd.DataFrame()

        except Exception:

            data[name] = pd.DataFrame()

    return data


def get_dataset_summary(data):
    """
    Return the number of records
    in each customer dataset.
    """

    summary = {}

    for name, dataframe in data.items():

        summary[name] = len(dataframe)

    return summary


def get_customer_reviews(data):
    """
    Return the reviews dataset.
    """

    return data.get(
        "reviews",
        pd.DataFrame()
    )


def get_customer_purchases(data):
    """
    Return the purchases dataset.
    """

    return data.get(
        "purchases",
        pd.DataFrame()
    )


def get_customer_interactions(data):
    """
    Return the interactions dataset.
    """

    return data.get(
        "interactions",
        pd.DataFrame()
    )


def get_customer_sessions(data):
    """
    Return the sessions dataset.
    """

    return data.get(
        "sessions",
        pd.DataFrame()
    )


def get_users(data):
    """
    Return the users dataset.
    """

    return data.get(
        "users",
        pd.DataFrame()
    )