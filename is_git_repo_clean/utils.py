# ------- #
# Imports #
# ------- #

from asyncio import gather
from types import SimpleNamespace as o


# ---- #
# Main #
# ---- #


#
# I like to think the common use-case for 'gather' is to cancel all async
#   operations should any one of them fail.  This is not how 'gather' was
#   implemented though which is why I wrote this function
#
async def resolveAll(awaitables):
    gatherAll = None
    try:
        gatherAll = gather(*awaitables)
        result = await gatherAll
    finally:
        if gatherAll:
            gatherAll.cancel()

    return result


#
# I have no idea what to name this.  Python just doesn't have a clean ternary
#   operator which stinks and I didn't want to use 'iif' because that's less
#   readable.  So for now we have a verbose and less performant, but readable
#   function chain
#


def whenTruthy(condition):
    def return_(truthyResult):
        def otherwise(falseyResult):
            if condition:
                return truthyResult
            else:
                return falseyResult

        return o(otherwise=otherwise)

    return o(return_=return_)


def iif(condition, whenTruthy, whenFalsey):
    if condition:
        return whenTruthy
    else:
        return whenFalsey
