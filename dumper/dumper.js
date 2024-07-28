// const { MongoClient } = require('mongodb');
// const fs = require('fs').promises;

// async function transferData() {
//   const sourceUri = 'mongodb+srv://Phenzic:anotherpassword@cluster2.hxp8umw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster2';
//   const targetUri = 'mongodb+srv://ogungbolamayowa:XaDjvf4CqoZV1Ler@cluster0.tz1beoy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0';

//   const sourceClient = new MongoClient(sourceUri);
//   const targetClient = new MongoClient(targetUri);

//   try {
//     await sourceClient.connect();
//     await targetClient.connect();

//     const sourceDb = sourceClient.db('db');
//     const targetDb = targetClient.db('vaults');

//     const collections = await sourceDb.listCollections().toArray();

//     for (const collection of collections) {
//       const data = await sourceDb.collection(collection.name).find().toArray();
//       if (data.length > 0) {
//         await targetDb.collection(collection.name).insertMany(data);

//         // Write the data to a file
//         const fileName = `${collection.name}.json`;
//         await fs.writeFile(fileName, JSON.stringify(data, null, 2));
//         console.log(`Data from collection ${collection.name} written to file ${fileName}`);
//       }
//     }
//   } finally {
//     await sourceClient.close();
//     await targetClient.close();
//   }
// }

// transferData().catch(console.error);





const { MongoClient } = require('mongodb');
const fs = require('fs').promises;


// mongodb+srv://<username>:<password>@cluster1.ze89abk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1

async function fetchData() {
  const sourceUri = 'mongodb+srv://Phenzic:anotherpassword@cluster1.ze89abk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1';
  const sourceClient = new MongoClient(sourceUri);

  try {
    await sourceClient.connect();
    const sourceDb = sourceClient.db('client');
    const collections = await sourceDb.listCollections().toArray();

    for (const collection of collections) {
      const data = await sourceDb.collection(collection.name).find().toArray();
      if (data.length > 0) {
        const fileName = `${collection.name}.json`;
        await fs.writeFile(fileName, JSON.stringify(data, null, 2));
        console.log(`Data from collection ${collection.name} written to file ${fileName}`);
      }
    }
  } finally {
    await sourceClient.close();
  }
}

async function uploadData() {
  const targetUri = 'mongodb+srv://ogungbolamayowa:XaDjvf4CqoZV1Ler@cluster0.tz1beoy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0';
  const targetClient = new MongoClient(targetUri);

  try {
    await targetClient.connect();
    const targetDb = targetClient.db('wallet');
    const files = await fs.readdir('.');

    for (const file of files) {
      if (file.endsWith('.json')) {
        const data = JSON.parse(await fs.readFile(file, 'utf-8'));
        const collectionName = file.replace('.json', '');
        if (data.length > 0) {
          await targetDb.collection(collectionName).insertMany(data);
          console.log(`Data from file ${file} inserted into collection ${collectionName}`);
        }
      }
    }
  } finally {
    await targetClient.close();
  }
}

// Usage
// fetchData().catch(console.error);
// After making local changes, run uploadData()
uploadData().catch(console.error);
