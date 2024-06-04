"""Main file for address api endpoints.
CRUD functions and specific searches are included.
"""
import logging
from fastapi import APIRouter, HTTPException, status, Depends
from api.models.address import Address
from api.schemas.address import (GetAddress,
                                 PostAddress,
                                 UpdateAddress,
                                 SearchChoices)
from logger import LogHandler

address_router = APIRouter(prefix="/api/address", tags=["address"])
LogHandler('activity-logs')
logger = logging.getLogger('activity-logs')


@address_router.get("/all")
async def get_all_address():
    """Function to get all address from database."""
    try:
        data = Address.all()
        return await GetAddress.from_queryset(data)
    except Exception as e:
        logger.error('Error on getting all address. {}'.format(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Error on getting all address. {}'.format(e)
        )


@address_router.get("/search/range/{min_long}/{max_long}/{min_lat}/{max_lat}")
async def get_address_range(min_long: float,
                            max_long: float,
                            min_lat: float,
                            max_lat: float):
    """Function to get specific addresses by range of coordinates.
    Maximum(max_) values should be greater than Minimum(min_) values."""
    retval = list()

    try:
        if max_long < min_long or max_lat < min_lat:
            # Checking for minimum and maximum values
            logger.warning("Invalid Coordinate combinations")
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail='Max values should be Greater than Min Values'
            )

        query = Address.all()
        data = await GetAddress.from_queryset(query)

        for row in data:
            # Loop for checking individual coordinates per address
            temp_dict = row.model_dump()
            longtitude = temp_dict.get('longtitude', 0)
            latitude = temp_dict.get('latitude', 0)

            if (
                min_long <= longtitude <= max_long and
                min_lat <= latitude <= max_lat
            ):
                retval.append(row)
    except Exception as e:
        logger.error('Error on getting address range. Details: {}'.format(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Error on getting address range. {}'.format(e)
        )

    return retval


@address_router.get("/search")
async def get_address_custom(data: SearchChoices = Depends()):
    """Function to get address with specific fields.
       Addresses can be search by country, region, province,
       city, street or zipcode. Casing must be exact.
    """
    param_dict = data.model_dump()  # converts pydantic model to dictionary
    param_choice = param_dict.get('choice', '')
    param_value = param_dict.get('search_value', '')

    try:
        if param_choice.lower().strip() == 'city':
            return await GetAddress.from_queryset(Address.filter(
                city=param_value))
        elif param_choice.lower().strip() == 'province':
            return await GetAddress.from_queryset(Address.filter(
                province=param_value))
        elif param_choice.lower().strip() == 'region':
            return await GetAddress.from_queryset(Address.filter(
                region=param_value))
        elif param_choice.lower().strip() == 'country':
            return await GetAddress.from_queryset(Address.filter(
                country=param_value))
        elif param_choice.lower().strip() == 'street':
            return await GetAddress.from_queryset(Address.filter(
                street=param_value))
        elif param_choice.lower().strip() == 'zipcode':
            return await GetAddress.from_queryset(Address.filter(
                zipcode=param_value))
    except Exception as e:
        logger.error('Error on getting custom search. {}'.format(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Error on getting custom search. {}'.format(e)
        )


@address_router.post("/post")
async def post_address(body: PostAddress):
    """Function for inserting Address to database.
    Has checking for blank or zero values."""
    valid_data = True
    data = body.model_dump(exclude_unset=True)
    str_keys = ['name',
                'country',
                'region',
                'province',
                'city',
                'street',
                'unit name']
    inv_key_list = list()
    inv_val_list = list()

    try:
        for k, v in data.items():
            if k in str_keys and v == "":
                valid_data = False
                inv_key_list.append(k)
                inv_val_list.append(v)

            if k == "zipcode" and v == 0:
                valid_data = False
                inv_key_list.append(k)
                inv_val_list.append(v)

            if k == 'longtitude':
                if v > 180 or v < -180:
                    valid_data = False
                    inv_key_list.append(k)
                    inv_val_list.append(v)

            if k == 'latitude':
                if v > 90 or v < -90:
                    valid_data = False
                    inv_key_list.append(k)
                    inv_val_list.append(v)

        if valid_data:
            row = await Address.create(**body.model_dump(exclude_unset=True))
            return await GetAddress.from_tortoise_orm(row)
        else:
            logger.error(
                'fields ({}) have invalid values ({})'.format(
                    inv_key_list,
                    inv_val_list
                    )
            )
            detail_text = "fields ({}) have invalid values ({})".format(
                inv_key_list,
                inv_val_list
            )
            raise HTTPException(
                status_code=status.HTTP_417_EXPECTATION_FAILED,
                detail=detail_text
            )
    except Exception as e:
        logger.error(
            'Error on posting address to database. Details: {}'.format(e))
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Error on posting address to database'
            )


@address_router.put("/update/{key}")
async def update_address(key: int, body: UpdateAddress):
    """Function for updating specific address fields.
       All values can be updated except the primary key.
       Fields can be removed if not planned to be updated."""

    try:
        data = body.model_dump(exclude_unset=True)
        valid_data = True
        str_keys = ['name',
                    'country',
                    'region',
                    'province',
                    'city',
                    'street',
                    'unit name']
        inv_key_list = list()
        inv_val_list = list()
        for k, v in data.items():  # loop for checking fields with empty values
            if k in str_keys and v == "":
                valid_data = False
                inv_key_list.append(k)
                inv_val_list.append(v)

            if k == "zipcode" and v == 0:
                valid_data = False
                inv_key_list.append(k)
                inv_val_list.append(v)

            if k == 'longtitude':  # checking if longtitude values are valid
                if v > 180 or v < -180:
                    valid_data = False
                    inv_key_list.append(k)
                    inv_val_list.append(v)

            if k == 'latitude':  # checking if latitude values are valid
                if v > 90 or v < -90:
                    valid_data = False
                    inv_key_list.append(k)
                    inv_val_list.append(v)

        exists = await Address.filter(id=key).exists()
        if not exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address Not Found"
            )

        if not valid_data:
            detail_text = "fields ({}) have invalid values ({})".format(
                inv_key_list,
                inv_val_list
            )
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=detail_text
            )

        await Address.filter(id=key).update(**data)

        return await GetAddress.from_queryset_single(Address.get(id=key))

    except Exception as e:
        logger.error('Error on updating Address. Details:{}'.format(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error on updating Address. {}'.format(e)
        )


@address_router.delete("/delete/{key}")
async def delete_address(key: int):
    """Function for deleting data in database.
    Deletion is based on address id.
    """
    try:
        exists = await Address.filter(id=key).exists()
        if not exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address Not Found"
            )
        await Address.filter(id=key).delete()
        return "Address ID number {} Deleted.".format(key)
    except Exception as e:
        logger.error('Error on deleting data. Details: {}'.format(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error on deleting data'
        )
