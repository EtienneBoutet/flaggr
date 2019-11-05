/**
 * Challenge model
 */
export class Challenge {
  public id: number;
  public name: string;
  public description: string;
  public points: number;
  public solves: number;
  public files: string[];
  public links: string[];
  public tags: string[];
  public isSolved: boolean;

  constructor() {
    this.id = -1;
    this.name = '';
    this.description = '';
    this.points = 0;
    this.solves = 0;
    this.files = [];
    this.links = [];
    this.tags = [];
    this.isSolved = false;
  }
}
