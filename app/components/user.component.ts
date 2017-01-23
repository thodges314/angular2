import {Component} from '@angular/core';

@Component({
  selector: 'user',
  template: `
  <h1>{{name}}</h1>
  <p><strong>Email:</strong> {{email}}</p>
  <p><strong>Address:</strong> {{address.street}} {{address.city}} {{address.state}}</p>
  <button (click) = "toggleHobbies()">{{showHobbies? "hide hobbies" : "show hobbies"}}</button>
  <div *ngIf = "showHobbies">
    <h3>Hobbies</h3>
    <ul>
      <li *ngFor = "let hobby of hobbies; let i = index">
        {{hobby}} <button (click)="deleteHobby(i)">X</button>
      </li>
    </ul>
    <form (submit)="addHobby(hobby.value)">
      <label>add hobby:</label><br />
      <input type="text" #hobby /><br />
    </form>
  </div>
  <hr />
  <h3>edit user:</h3>
  <form>
    <label>name: </label><br />
    <input type="text"  name="name" [(ngModel)]="name" /> <br/>
    <label>eMail: </label><br />
    <input type="text"  name="email" [(ngModel)]="email" /> <br/>
    <label>street address: </label><br />
    <input type="text"  name="address.street" [(ngModel)]="address.street" /> <br/>
    <label>city: </label><br />
    <input type="text"  name="address.city" [(ngModel)]="address.city" /> <br/>
    <label>state: </label><br />
    <input type="text"  name="address.state" [(ngModel)]="address.state" /> <br/>
  </form>
  `,
})
export class UserComponent {
  name: string;
  email: string;
  address: address;
  hobbies: string[];
  showHobbies: boolean;

  constructor() {
    this.name = 'Thomas';
    this.email = 'thodges@javascriptonline.org';
    this.address = {
      street: '2125 Benicia Ct',
      city: 'Davis',
      state: 'CA'
    };
    this.hobbies = ['books', 'photography', 'bicycling'];
    this.showHobbies = false;
  }

  toggleHobbies(){
    this.showHobbies = !this.showHobbies;
  }

  addHobby(hobby: string) {
    this.hobbies.push(hobby);
  }

  deleteHobby(index: int){
    this.hobbies.splice(index, 1);
  }
}

interface address {
  street: string;
  city: string;
  state: string;
}
