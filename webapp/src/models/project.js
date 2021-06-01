export default class Project {
  constructor (map) {
    this.uuid = map.uuid
    this.name = map.name
    this.company_id = map.company_id
    this.description = map.description
    this.start_date = map.start_date
    this.end_date = map.end_date
    const members = map.members
    this.members = members.map(member => new ProjectMember(member))
  }

  getMembers () {
    return Array.prototype.map.call(this.members, (s) => s.name).toString()
  }
}

export class ProjectMember {
  constructor (map) {
    this.id = map.id
    this.name = map.name
  }
}
