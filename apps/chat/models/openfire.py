# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class OfConParticipant(models.Model):
    conversationid = models.IntegerField()
    joineddate = models.BigIntegerField()
    leftdate = models.BigIntegerField(blank=True, null=True)
    barejid = models.CharField(max_length=255)
    jidresource = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ofconparticipant'


class OfConversation(models.Model):
    conversationid = models.IntegerField(primary_key=True)
    room = models.CharField(max_length=1024, blank=True, null=True)
    isexternal = models.SmallIntegerField()
    startdate = models.BigIntegerField()
    lastactivity = models.BigIntegerField()
    messagecount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ofconversation'


class OfExtComponentConf(models.Model):
    subdomain = models.CharField(primary_key=True, max_length=255)
    wildcard = models.IntegerField()
    secret = models.CharField(max_length=255, blank=True, null=True)
    permission = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'ofextcomponentconf'


class OfGroup(models.Model):
    groupname = models.CharField(primary_key=True, max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ofgroup'


class OfGroupProp(models.Model):
    groupname = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=100)
    propvalue = models.TextField()

    class Meta:
        managed = False
        db_table = 'ofgroupprop'
        unique_together = (('groupname', 'name'),)


class OfGroupUser(models.Model):
    groupname = models.CharField(primary_key=True, max_length=50)
    username = models.CharField(max_length=100)
    administrator = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ofgroupuser'
        unique_together = (('groupname', 'username', 'administrator'),)


class OfId(models.Model):
    idtype = models.IntegerField(primary_key=True)
    id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ofid'


class OfMessageArchive(models.Model):
    messageid = models.BigIntegerField(blank=True, null=True)
    conversationid = models.IntegerField()
    fromjid = models.CharField(max_length=1024)
    fromjidresource = models.CharField(max_length=1024, blank=True, null=True)
    tojid = models.CharField(max_length=1024)
    tojidresource = models.CharField(max_length=1024, blank=True, null=True)
    sentdate = models.BigIntegerField()
    stanza = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ofmessagearchive'


class OfMucAffiliation(models.Model):
    roomid = models.IntegerField(primary_key=True)
    jid = models.CharField(max_length=1024)
    affiliation = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ofmucaffiliation'
        unique_together = (('roomid', 'jid'),)


class OfMucConversationLog(models.Model):
    roomid = models.IntegerField()
    messageid = models.IntegerField()
    sender = models.CharField(max_length=1024)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    logtime = models.CharField(max_length=15)
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    stanza = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ofmucconversationlog'


class OfMucMember(models.Model):
    roomid = models.IntegerField(primary_key=True)
    jid = models.CharField(max_length=1024)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    firstname = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    faqentry = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ofmucmember'
        unique_together = (('roomid', 'jid'),)


class OfMucRoom(models.Model):
    serviceid = models.IntegerField(primary_key=True)
    roomid = models.IntegerField()
    creationdate = models.CharField(max_length=15)
    modificationdate = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    naturalname = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    lockeddate = models.CharField(max_length=15)
    emptydate = models.CharField(max_length=15, blank=True, null=True)
    canchangesubject = models.IntegerField()
    maxusers = models.IntegerField()
    publicroom = models.IntegerField()
    moderated = models.IntegerField()
    membersonly = models.IntegerField()
    caninvite = models.IntegerField()
    roompassword = models.CharField(max_length=50, blank=True, null=True)
    candiscoverjid = models.IntegerField()
    logenabled = models.IntegerField()
    subject = models.CharField(max_length=100, blank=True, null=True)
    rolestobroadcast = models.IntegerField()
    usereservednick = models.IntegerField()
    canchangenick = models.IntegerField()
    canregister = models.IntegerField()
    allowpm = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ofmucroom'
        unique_together = (('serviceid', 'name'),)


class OfmMucRoomProp(models.Model):
    roomid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    propvalue = models.TextField()

    class Meta:
        managed = False
        db_table = 'ofmucroomprop'
        unique_together = (('roomid', 'name'),)


class OfMucService(models.Model):
    serviceid = models.IntegerField()
    subdomain = models.CharField(primary_key=True, max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    ishidden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ofmucservice'


class OfMucServiceProp(models.Model):
    serviceid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    propvalue = models.TextField()

    class Meta:
        managed = False
        db_table = 'ofmucserviceprop'
        unique_together = (('serviceid', 'name'),)


class OfOffline(models.Model):
    username = models.CharField(primary_key=True, max_length=64)
    messageid = models.IntegerField()
    creationdate = models.CharField(max_length=15)
    messagesize = models.IntegerField()
    stanza = models.TextField()

    class Meta:
        managed = False
        db_table = 'ofoffline'
        unique_together = (('username', 'messageid'),)


class OfPresence(models.Model):
    username = models.CharField(primary_key=True, max_length=64)
    offlinepresence = models.TextField(blank=True, null=True)
    offlinedate = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'ofpresence'


class OfPrivacyList(models.Model):
    username = models.CharField(primary_key=True, max_length=64)
    name = models.CharField(max_length=100)
    isdefault = models.IntegerField()
    list = models.TextField()

    class Meta:
        managed = False
        db_table = 'ofprivacylist'
        unique_together = (('username', 'name'),)


class OfProperty(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    propvalue = models.CharField(max_length=4000)
    encrypted = models.IntegerField(blank=True, null=True)
    iv = models.CharField(max_length=24, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ofproperty'


class OfPubSubAffiliation(models.Model):
    serviceid = models.CharField(primary_key=True, max_length=100)
    nodeid = models.CharField(max_length=100)
    jid = models.CharField(max_length=1024)
    affiliation = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'ofpubsubaffiliation'
        unique_together = (('serviceid', 'nodeid', 'jid'),)


class OfPubSubDefaultConf(models.Model):
    serviceid = models.CharField(primary_key=True, max_length=100)
    leaf = models.IntegerField()
    deliverpayloads = models.IntegerField()
    maxpayloadsize = models.IntegerField()
    persistitems = models.IntegerField()
    maxitems = models.IntegerField()
    notifyconfigchanges = models.IntegerField()
    notifydelete = models.IntegerField()
    notifyretract = models.IntegerField()
    presencebased = models.IntegerField()
    senditemsubscribe = models.IntegerField()
    publishermodel = models.CharField(max_length=15)
    subscriptionenabled = models.IntegerField()
    accessmodel = models.CharField(max_length=10)
    language = models.CharField(max_length=255, blank=True, null=True)
    replypolicy = models.CharField(max_length=15, blank=True, null=True)
    associationpolicy = models.CharField(max_length=15)
    maxleafnodes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ofpubsubdefaultconf'
        unique_together = (('serviceid', 'leaf'),)


class OfPubSubitem(models.Model):
    serviceid = models.CharField(primary_key=True, max_length=100)
    nodeid = models.CharField(max_length=100)
    id = models.CharField(max_length=100)
    jid = models.CharField(max_length=1024)
    creationdate = models.CharField(max_length=15)
    payload = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ofpubsubitem'
        unique_together = (('serviceid', 'nodeid', 'id'),)


class OfPubSubNode(models.Model):
    serviceid = models.CharField(primary_key=True, max_length=100)
    nodeid = models.CharField(max_length=100)
    leaf = models.IntegerField()
    creationdate = models.CharField(max_length=15)
    modificationdate = models.CharField(max_length=15)
    parent = models.CharField(max_length=100, blank=True, null=True)
    deliverpayloads = models.IntegerField()
    maxpayloadsize = models.IntegerField(blank=True, null=True)
    persistitems = models.IntegerField(blank=True, null=True)
    maxitems = models.IntegerField(blank=True, null=True)
    notifyconfigchanges = models.IntegerField()
    notifydelete = models.IntegerField()
    notifyretract = models.IntegerField()
    presencebased = models.IntegerField()
    senditemsubscribe = models.IntegerField()
    publishermodel = models.CharField(max_length=15)
    subscriptionenabled = models.IntegerField()
    configsubscription = models.IntegerField()
    accessmodel = models.CharField(max_length=10)
    payloadtype = models.CharField(max_length=100, blank=True, null=True)
    bodyxslt = models.CharField(max_length=100, blank=True, null=True)
    dataformxslt = models.CharField(max_length=100, blank=True, null=True)
    creator = models.CharField(max_length=1024)
    description = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    replypolicy = models.CharField(max_length=15, blank=True, null=True)
    associationpolicy = models.CharField(max_length=15, blank=True, null=True)
    maxleafnodes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ofpubsubnode'
        unique_together = (('serviceid', 'nodeid'),)


class OfPubSubNodeGroups(models.Model):
    serviceid = models.CharField(max_length=100)
    nodeid = models.CharField(max_length=100)
    rostergroup = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ofpubsubnodegroups'


class OfPubSubNodeJids(models.Model):
    serviceid = models.CharField(primary_key=True, max_length=100)
    nodeid = models.CharField(max_length=100)
    jid = models.CharField(max_length=1024)
    associationtype = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ofpubsubnodejids'
        unique_together = (('serviceid', 'nodeid', 'jid'),)


class OfPubSubSubscription(models.Model):
    serviceid = models.CharField(primary_key=True, max_length=100)
    nodeid = models.CharField(max_length=100)
    id = models.CharField(max_length=100)
    jid = models.CharField(max_length=1024)
    owner = models.CharField(max_length=1024)
    state = models.CharField(max_length=15)
    deliver = models.IntegerField()
    digest = models.IntegerField()
    digest_frequency = models.IntegerField()
    expire = models.CharField(max_length=15, blank=True, null=True)
    includebody = models.IntegerField()
    showvalues = models.CharField(max_length=30)
    subscriptiontype = models.CharField(max_length=10)
    subscriptiondepth = models.IntegerField()
    keyword = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ofpubsubsubscription'
        unique_together = (('serviceid', 'nodeid', 'id'),)


class OfRemoteServerConf(models.Model):
    xmppdomain = models.CharField(primary_key=True, max_length=255)
    remoteport = models.IntegerField(blank=True, null=True)
    permission = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'ofremoteserverconf'


class OfRoster(models.Model):
    rosterid = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=64)
    jid = models.CharField(max_length=1024)
    sub = models.IntegerField()
    ask = models.IntegerField()
    recv = models.IntegerField()
    nick = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ofroster'


class OfRosterGroups(models.Model):
    rosterid = models.OneToOneField(OfRoster, models.DO_NOTHING, db_column='rosterid', primary_key=True)
    rank = models.IntegerField()
    groupname = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ofrostergroups'
        unique_together = (('rosterid', 'rank'),)


class OfRrds(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    updateddate = models.BigIntegerField()
    bytes = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ofrrds'


class OfSaslAuthorized(models.Model):
    username = models.CharField(primary_key=True, max_length=64)
    principal = models.CharField(max_length=4000)

    class Meta:
        managed = False
        db_table = 'ofsaslauthorized'
        unique_together = (('username', 'principal'),)


class OfSecurityAuditlog(models.Model):
    msgid = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=64)
    entrystamp = models.BigIntegerField()
    summary = models.CharField(max_length=255)
    node = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ofsecurityauditlog'


class OfUser(models.Model):
    username = models.CharField(primary_key=True, max_length=64)
    storedkey = models.CharField(max_length=32, blank=True, null=True)
    serverkey = models.CharField(max_length=32, blank=True, null=True)
    salt = models.CharField(max_length=32, blank=True, null=True)
    iterations = models.IntegerField(blank=True, null=True)
    plainpassword = models.CharField(max_length=32, blank=True, null=True)
    encryptedpassword = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    creationdate = models.CharField(max_length=15)
    modificationdate = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'ofuser'


class OfUserFlag(models.Model):
    username = models.CharField(primary_key=True, max_length=64)
    name = models.CharField(max_length=100)
    starttime = models.CharField(max_length=15, blank=True, null=True)
    endtime = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ofuserflag'
        unique_together = (('username', 'name'),)


class OfUserProp(models.Model):
    username = models.CharField(primary_key=True, max_length=64)
    name = models.CharField(max_length=100)
    propvalue = models.TextField()

    class Meta:
        managed = False
        db_table = 'ofuserprop'
        unique_together = (('username', 'name'),)


class OfVCard(models.Model):
    username = models.CharField(primary_key=True, max_length=64)
    vcard = models.TextField()

    class Meta:
        managed = False
        db_table = 'ofvcard'


class OfVersion(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ofversion'
