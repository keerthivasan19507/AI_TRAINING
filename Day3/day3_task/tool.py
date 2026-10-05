def calculate_marks(marks):
    """
    Calculate total marks and percentage.

    The maximum mark is 20 for each subject.
    """

    try:
        total = sum(marks)
        maximum = len(marks) * 20
        percentage = (total / maximum) * 100

        return (
            f"Total marks: {total}/{maximum}\n"
            f"Percentage: {percentage:.2f}%"
        )

    except Exception as e:
        return f"Tool error: {str(e)}"