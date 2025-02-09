import json
from quart import Blueprint, Response, request
from rental.models.modelsClass import RentalModel

deleterentalb = Blueprint('delete_current_rental', __name__,)

@deleterentalb.route('/api/v1/rental/<string:rentalUid>', methods=['DELETE'])
async def delete_current_rental(rentalUid: str) -> Response:
    try:
        rental = RentalModel.select().where(RentalModel.rental_uid == rentalUid).get()

        if rental.status != 'IN_PROGRESS':
            return Response(status=403, content_type='application/json', response=json.dumps({'errors': ['Rental not in progres.']}))

        rental.status = 'CANCELED'
        rental.save()

        return Response(status=200, content_type='application/json', response=json.dumps(rental.to_dict()))
    except Exception as e:
        return Response(status=404, content_type='application/json', response=json.dumps({'errors': ['No Uid found']}))
