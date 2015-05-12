from sqlalchemy.ext.automap import automap_base

# automap base
Base = automap_base()

# pre-declare User for the 'user' table
class User(Base):
    __tablename__ = 'user'

    # override schema elements like Columns
    user_name = Column('name', String)

    # override relationships too, if desired.
    # we must use the same name that automap would use for the
    # relationship, and also must refer to the class name that automap will
    # generate for "address"
    address_collection = relationship("address", collection_class=set)