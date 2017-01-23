import {Component} from '@angular/core';

@Component({
  selector: 'user',
  template: `
  <h1>Hello, {{name}}</h1>
  <p><strong>Email:</strong> {{email}}</p>
  <p><strong>Address:</strong> {{address.street}} {{address.city}} {{address.state}}</p>
  <button (click) = "toggleHobbies()">{{showHobbies? "hide hobbies" : "show hobbies"}}</button>
  <div *ngIf = "showHobbies">
    <h3>Hobbies</h3>
    <ul>
      <li *ngFor = "let hobby of hobbies">
        {{hobby}}
      </li>
    </ul>
  </div>
  <form>
    <label>name: </label><br />
    <input type="text"  name="name" [(ngModel)]="name" /> 
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
}

interface address {
  street: string;
  city: string;
  state: string;
}
